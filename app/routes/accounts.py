from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import (
    AccountType, Account, SubAccount, AccountSubAccount,
    FiscalPeriod, JournalVoucher, SubaccountEntry,
)

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")


# ── Journal Vouchers ─────────────────────────────────────────────────────

@accounts_bp.route("/")
@login_required
def list_vouchers():
    vouchers = JournalVoucher.query.order_by(JournalVoucher.transaction_datetime.desc()).limit(200).all()
    return render_template("accounts/list.html", vouchers=vouchers)


@accounts_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_voucher():
    if request.method == "POST":
        acc_sub_acc_ids = request.form.getlist("acc_sub_acc_id")
        entry_types = request.form.getlist("entry_type")
        amounts = request.form.getlist("amount")

        lines = []
        for asa_id, etype, amt_raw in zip(acc_sub_acc_ids, entry_types, amounts):
            if not asa_id or not amt_raw:
                continue
            try:
                amt = Decimal(amt_raw)
            except InvalidOperation:
                continue
            if amt <= 0:
                continue
            lines.append((int(asa_id), etype, amt))

        if len(lines) < 2:
            flash("A journal voucher needs at least two lines (one debit, one credit).", "error")
            return redirect(url_for("accounts.new_voucher"))

        total_debit = sum((amt for _, t, amt in lines if t == "Debit"), Decimal("0"))
        total_credit = sum((amt for _, t, amt in lines if t == "Credit"), Decimal("0"))
        if total_debit != total_credit:
            flash(f"Debits (KES {total_debit:,.2f}) must equal credits (KES {total_credit:,.2f}) — not saved.", "error")
            return redirect(url_for("accounts.new_voucher"))

        period = FiscalPeriod.get_or_create_current()
        voucher = JournalVoucher(
            description=request.form["description"].strip(),
            source_reference=request.form.get("source_reference") or None,
            fiscal_period_id=period.fiscal_period_id,
            created_by=current_user.system_user_id,
        )
        db.session.add(voucher)
        db.session.flush()

        for asa_id, etype, amt in lines:
            db.session.add(SubaccountEntry(
                journal_voucher_id=voucher.journal_voucher_id,
                acc_sub_acc_id=asa_id,
                entry_type=etype,
                amount=amt,
                fiscal_period_id=period.fiscal_period_id,
            ))

        db.session.commit()
        flash(f"Journal voucher posted — {len(lines)} lines, KES {total_debit:,.2f} balanced.", "success")
        return redirect(url_for("accounts.list_vouchers"))

    return render_template(
        "accounts/new_voucher.html",
        acc_sub_accs=AccountSubAccount.query.join(Account).order_by(Account.account_no).all(),
    )


@accounts_bp.route("/<int:journal_voucher_id>")
@login_required
def view_voucher(journal_voucher_id):
    voucher = JournalVoucher.query.get_or_404(journal_voucher_id)
    return render_template("accounts/view_voucher.html", voucher=voucher)


# ── Chart of Accounts ────────────────────────────────────────────────────

@accounts_bp.route("/chart")
@login_required
def chart_of_accounts():
    accounts = Account.query.order_by(Account.account_no).all()
    return render_template("accounts/chart.html", accounts=accounts)


@accounts_bp.route("/chart/new", methods=["GET", "POST"])
@login_required
def new_account():
    if request.method == "POST":
        account = Account(
            account_no=request.form["account_no"].strip(),
            name=request.form["name"].strip(),
            account_type_id=request.form["account_type_id"],
        )
        db.session.add(account)
        db.session.commit()
        flash(f"Account '{account.account_no} — {account.name}' created.", "success")
        return redirect(url_for("accounts.chart_of_accounts"))
    return render_template("accounts/account_form.html", account_types=AccountType.query.order_by(AccountType.account_type_id).all())


# ── Sub-Accounts ─────────────────────────────────────────────────────────

@accounts_bp.route("/sub-accounts")
@login_required
def list_sub_accounts():
    sub_accounts = SubAccount.query.order_by(SubAccount.name).all()
    return render_template("accounts/sub_accounts.html", sub_accounts=sub_accounts)


@accounts_bp.route("/sub-accounts/new", methods=["GET", "POST"])
@login_required
def new_sub_account():
    if request.method == "POST":
        sub_account = SubAccount(name=request.form["name"].strip())
        db.session.add(sub_account)
        db.session.commit()
        flash(f"Sub-account '{sub_account.name}' created.", "success")
        return redirect(url_for("accounts.list_sub_accounts"))
    return render_template("accounts/sub_account_form.html")


@accounts_bp.route("/sub-accounts/<int:sub_account_id>/link", methods=["GET", "POST"])
@login_required
def link_sub_account(sub_account_id):
    sub_account = SubAccount.query.get_or_404(sub_account_id)

    if request.method == "POST":
        account_id = request.form.get("account_id")
        if AccountSubAccount.query.filter_by(account_id=account_id, sub_account_id=sub_account.sub_account_id).first():
            flash("Already linked to that account.", "error")
        else:
            db.session.add(AccountSubAccount(account_id=account_id, sub_account_id=sub_account.sub_account_id))
            db.session.commit()
            flash(f"Linked '{sub_account.name}' to the selected account.", "success")
        return redirect(url_for("accounts.list_sub_accounts"))

    linked_account_ids = {l.account_id for l in AccountSubAccount.query.filter_by(sub_account_id=sub_account.sub_account_id).all()}
    available = [a for a in Account.query.order_by(Account.account_no).all() if a.account_id not in linked_account_ids]
    return render_template("accounts/link_sub_account.html", sub_account=sub_account, available=available)


# ── Ledger view (per sub-account, across all vouchers) ──────────────────

@accounts_bp.route("/ledger/<int:acc_sub_acc_id>")
@login_required
def ledger(acc_sub_acc_id):
    asa = AccountSubAccount.query.get_or_404(acc_sub_acc_id)
    entries = (
        SubaccountEntry.query
        .filter_by(acc_sub_acc_id=acc_sub_acc_id)
        .order_by(SubaccountEntry.transaction_datetime)
        .all()
    )
    running = Decimal("0")
    rows = []
    for e in entries:
        running += e.amount if e.entry_type == "Debit" else -e.amount
        rows.append((e, running))
    return render_template("accounts/ledger.html", asa=asa, rows=rows, balance=running)


# ── Fiscal Periods (read/admin) ──────────────────────────────────────────

@accounts_bp.route("/periods")
@login_required
def list_periods():
    periods = FiscalPeriod.query.order_by(FiscalPeriod.start_date.desc()).all()
    return render_template("accounts/periods.html", periods=periods)
