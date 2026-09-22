from datetime import datetime, timezone
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import PurchaseOrder, PurchaseOrderItem, GRN, GRNItem, Supplier, Product, StockMovement

procurement_bp = Blueprint("procurement", __name__, url_prefix="/procurement")


@procurement_bp.route("/")
@login_required
def list_purchase_orders():
    status = request.args.get("status", "open")
    query = PurchaseOrder.query
    if status == "open":
        query = query.filter_by(has_been_received=False)
    elif status == "received":
        query = query.filter_by(has_been_received=True)
    orders = query.order_by(PurchaseOrder.date_time_issued.desc()).limit(200).all()
    return render_template("procurement/list.html", orders=orders, status=status)


@procurement_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_purchase_order():
    if request.method == "POST":
        product_ids = request.form.getlist("product_id")
        quantities = request.form.getlist("quantity")
        rates = request.form.getlist("rate")

        lines = []
        for pid, qty_raw, rate_raw in zip(product_ids, quantities, rates):
            if not pid:
                continue
            product = Product.query.get(pid)
            if not product:
                continue
            qty = int(qty_raw or 1)
            rate = Decimal(rate_raw or "0")
            lines.append((product, qty, rate))

        if not lines:
            flash("Add at least one item before saving.", "error")
            return redirect(url_for("procurement.new_purchase_order"))

        po = PurchaseOrder(
            supplier_id=request.form["supplier_id"],
            order_reference=request.form.get("order_reference") or None,
            terms_conditions=request.form.get("terms_conditions") or None,
            validity_date=request.form.get("validity_date") or None,
            prepared_by=current_user.system_user_id,
        )
        db.session.add(po)
        db.session.flush()

        for product, qty, rate in lines:
            db.session.add(PurchaseOrderItem(
                purchase_order_id=po.purchase_order_id,
                product_id=product.product_id,
                name=product.name,
                quantity=qty,
                rate=rate,
                amount=qty * rate,
            ))

        db.session.commit()
        flash(f"Purchase order {po.purchase_order_no} created.", "success")
        return redirect(url_for("procurement.list_purchase_orders"))

    return render_template(
        "procurement/new.html",
        suppliers=Supplier.query.filter_by(is_active=True).order_by(Supplier.name).all(),
        products=Product.query.filter_by(is_active=True).order_by(Product.name).all(),
    )


@procurement_bp.route("/<int:purchase_order_id>")
@login_required
def view_purchase_order(purchase_order_id):
    po = PurchaseOrder.query.get_or_404(purchase_order_id)
    return render_template("procurement/view.html", po=po)


@procurement_bp.route("/<int:purchase_order_id>/check", methods=["POST"])
@login_required
def check_purchase_order(purchase_order_id):
    po = PurchaseOrder.query.get_or_404(purchase_order_id)
    po.has_been_checked = True
    po.checked_by = current_user.system_user_id
    po.date_time_checked = datetime.now(timezone.utc)
    db.session.commit()
    flash(f"{po.purchase_order_no} marked as checked.", "success")
    return redirect(url_for("procurement.view_purchase_order", purchase_order_id=po.purchase_order_id))


# ── GRNs (Goods Received Notes) ──────────────────────────────────────────

@procurement_bp.route("/<int:purchase_order_id>/grn/new", methods=["GET", "POST"])
@login_required
def new_grn(purchase_order_id):
    po = PurchaseOrder.query.get_or_404(purchase_order_id)

    if request.method == "POST":
        grn = GRN(
            purchase_order_id=po.purchase_order_id,
            delivery_note_no=request.form.get("delivery_note_no") or None,
            ap_invoice_no=request.form.get("ap_invoice_no") or None,
            created_by=current_user.system_user_id,
        )
        db.session.add(grn)
        db.session.flush()

        any_received = False
        for item in po.items:
            qty_field = f"quantity_received_{item.purchase_order_item_id}"
            batch_field = f"batch_no_{item.purchase_order_item_id}"
            expiry_field = f"expiry_{item.purchase_order_item_id}"

            qty_received = int(request.form.get(qty_field, "0") or "0")
            if qty_received <= 0:
                continue
            any_received = True

            db.session.add(GRNItem(
                grn_id=grn.grn_id,
                purchase_order_item_id=item.purchase_order_item_id,
                product_id=item.product_id,
                quantity_ordered=item.quantity,
                quantity_received=qty_received,
                rate=item.rate,
                batch_no=request.form.get(batch_field) or None,
                earliest_expiry_date=request.form.get(expiry_field) or None,
            ))

        if not any_received:
            db.session.rollback()
            flash("Enter a received quantity for at least one item.", "error")
            return redirect(url_for("procurement.new_grn", purchase_order_id=po.purchase_order_id))

        po.has_been_received = True
        db.session.commit()
        flash(f"GRN {grn.grn_no} created — remember to commit it to stock.", "success")
        return redirect(url_for("procurement.view_grn", grn_id=grn.grn_id))

    return render_template("procurement/new_grn.html", po=po)


@procurement_bp.route("/grn/<int:grn_id>")
@login_required
def view_grn(grn_id):
    grn = GRN.query.get_or_404(grn_id)
    return render_template("procurement/view_grn.html", grn=grn)


@procurement_bp.route("/grn/<int:grn_id>/commit", methods=["POST"])
@login_required
def commit_grn(grn_id):
    grn = GRN.query.get_or_404(grn_id)
    if grn.is_committed_to_stock:
        flash("Already committed to stock.", "error")
        return redirect(url_for("procurement.view_grn", grn_id=grn.grn_id))

    for item in grn.items:
        item.product.quantity_in_stock += item.quantity_received
        db.session.add(StockMovement(
            product_id=item.product_id,
            supplier_id=grn.purchase_order.supplier_id,
            quantity_change=item.quantity_received,
            reason=f"GRN {grn.grn_no} — PO {grn.purchase_order.purchase_order_no}",
            recorded_by=current_user.system_user_id,
        ))

    grn.is_committed_to_stock = True
    db.session.commit()
    flash(f"{grn.grn_no} committed to stock.", "success")
    return redirect(url_for("procurement.view_grn", grn_id=grn.grn_id))
