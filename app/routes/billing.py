from datetime import datetime, timezone
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import (
    MedicalBill, BillItem, Service, Visit, Patient,
    AccountSubAccount, FiscalPeriod, JournalVoucher, SubaccountEntry,
)

billing_bp = Blueprint("billing", __name__, url_prefix="/billing")


@billing_bp.route("/")
@login_required
def list_bills():
    q = request.args.get("q", "").strip()
    query = MedicalBill.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(
                MedicalBill.medical_bill_no.ilike(like),
                MedicalBill.customer_name.ilike(like),
            )
        )
    bills = query.order_by(MedicalBill.date_time_created.desc()).limit(200).all()
    return render_template("billing/list.html", bills=bills, q=q)


@billing_bp.route("/visit/<int:visit_id>/new", methods=["GET", "POST"])
@login_required
def new_bill_for_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    patient = visit.patient

    if request.method == "POST":
        service_ids = request.form.getlist("service_id")
        quantities = request.form.getlist("quantity")

        if not service_ids:
            flash("Add at least one service before saving the bill.", "error")
            return redirect(url_for("billing.new_bill_for_visit", visit_id=visit.visit_id))

        bill = MedicalBill.get_or_create_for_visit(visit)

        for service_id, qty_raw in zip(service_ids, quantities):
            service = Service.query.get(service_id)
            if not service:
                continue
            bill.add_item(name=service.name, quantity=qty_raw, rate=service.cash_rate, service_id=service.service_id)

        visit.is_processed = True
        db.session.commit()

        flash(f"Bill {bill.medical_bill_no} updated for {patient.full_name} — running total KES {bill.total_bill_amount:,.2f}.", "success")
        return redirect(url_for("billing.list_bills"))

    return render_template(
        "billing/new.html",
        visit=visit,
        patient=patient,
        services=Service.query.filter_by(is_active=True).order_by(Service.name).all(),
    )


@billing_bp.route("/<int:medical_bill_id>")
@login_required
def view_bill(medical_bill_id):
    bill = MedicalBill.query.get_or_404(medical_bill_id)
    return render_template("billing/view.html", bill=bill)


@billing_bp.route("/<int:medical_bill_id>/pay", methods=["POST"])
@login_required
def record_payment(medical_bill_id):
    bill = MedicalBill.query.get_or_404(medical_bill_id)
    amount = Decimal(request.form.get("amount", "0") or "0")
    if amount <= 0:
        flash("Enter a payment amount greater than zero.", "error")
        return redirect(url_for("billing.view_bill", medical_bill_id=bill.medical_bill_id))

    bill.total_amount_paid = (bill.total_amount_paid or 0) + amount
    if bill.balance_due <= 0:
        bill.is_processed = True
        bill.date_time_processed = datetime.now(timezone.utc)

    gl_note = _post_payment_to_gl(bill, amount)
    db.session.commit()
    flash(f"Payment of KES {amount:,.2f} recorded.{gl_note}", "success")
    return redirect(url_for("billing.view_bill", medical_bill_id=bill.medical_bill_id))


def _post_payment_to_gl(bill, amount):
    """Debit Cash, Credit Service Revenue for a payment received. Looks up
    the default sub-accounts by name (seeded by migration/schema.sql) —
    if either has been renamed or deleted, this quietly skips posting
    rather than breaking the payment itself. Billing and Accounts are
    still two separate systems; this is a light integration, not a
    dependency — a payment must always be recordable even if the books
    aren't set up (yet, or on purpose)."""
    cash = AccountSubAccount.find_by_sub_account_name("Cash")
    revenue = AccountSubAccount.find_by_sub_account_name("Service Revenue")
    if not cash or not revenue:
        return " (GL posting skipped — default Cash/Service Revenue accounts not found; see Accounts settings.)"

    period = FiscalPeriod.get_or_create_current()
    voucher = JournalVoucher(
        description=f"Payment received — {bill.medical_bill_no}",
        source_reference=bill.medical_bill_no,
        fiscal_period_id=period.fiscal_period_id,
        created_by=current_user.system_user_id,
    )
    db.session.add(voucher)
    db.session.flush()
    db.session.add(SubaccountEntry(
        journal_voucher_id=voucher.journal_voucher_id, acc_sub_acc_id=cash.acc_sub_acc_id,
        entry_type="Debit", amount=amount, fiscal_period_id=period.fiscal_period_id,
    ))
    db.session.add(SubaccountEntry(
        journal_voucher_id=voucher.journal_voucher_id, acc_sub_acc_id=revenue.acc_sub_acc_id,
        entry_type="Credit", amount=amount, fiscal_period_id=period.fiscal_period_id,
    ))
    return ""


# ── Service catalog (simple admin CRUD) ─────────────────────────────────

@billing_bp.route("/services")
@login_required
def list_services():
    services = Service.query.order_by(Service.name).all()
    return render_template("billing/services.html", services=services)


@billing_bp.route("/services/new", methods=["GET", "POST"])
@login_required
def new_service():
    if request.method == "POST":
        service = Service(
            name=request.form["name"].strip(),
            cash_rate=Decimal(request.form.get("cash_rate", "0") or "0"),
        )
        db.session.add(service)
        db.session.commit()
        flash(f"Service '{service.name}' added.", "success")
        return redirect(url_for("billing.list_services"))
    return render_template("billing/service_form.html")
