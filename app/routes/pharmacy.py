from datetime import datetime, timezone
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Prescription, PrescriptionItem, Product, Visit, MedicalBill, StockMovement, Supplier

pharmacy_bp = Blueprint("pharmacy", __name__, url_prefix="/pharmacy")


@pharmacy_bp.route("/")
@login_required
def list_prescriptions():
    status = request.args.get("status", "pending")
    query = Prescription.query
    prescriptions = query.order_by(Prescription.created_at.desc()).limit(200).all()
    if status == "pending":
        prescriptions = [p for p in prescriptions if not p.is_fully_dispensed]
    elif status == "dispensed":
        prescriptions = [p for p in prescriptions if p.is_fully_dispensed]
    return render_template("pharmacy/list.html", prescriptions=prescriptions, status=status)


@pharmacy_bp.route("/visit/<int:visit_id>/new", methods=["GET", "POST"])
@login_required
def new_prescription(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    patient = visit.patient

    if request.method == "POST":
        product_ids = request.form.getlist("product_id")
        quantities = request.form.getlist("quantity")
        freqs = request.form.getlist("frequency_per_day")
        durations = request.form.getlist("dosage_duration")

        if not product_ids:
            flash("Add at least one medication before saving.", "error")
            return redirect(url_for("pharmacy.new_prescription", visit_id=visit.visit_id))

        prescription = Prescription(
            visit_id=visit.visit_id,
            patient_id=patient.patient_id,
            prescribed_by=request.form.get("prescribed_by") or None,
            special_instruction=request.form.get("special_instruction") or None,
        )
        db.session.add(prescription)
        db.session.flush()

        for product_id, qty_raw, freq, duration in zip(product_ids, quantities, freqs, durations):
            product = Product.query.get(product_id)
            if not product:
                continue
            db.session.add(PrescriptionItem(
                prescription_id=prescription.prescription_id,
                product_id=product.product_id,
                inscription=product.name,
                quantity=int(qty_raw or 1),
                frequency_per_day=freq or None,
                dosage_duration=duration or None,
            ))

        db.session.commit()
        flash(f"Prescription created for {patient.full_name}.", "success")
        next_url = request.args.get("next")
        return redirect(next_url or url_for("pharmacy.list_prescriptions"))

    return render_template(
        "pharmacy/new.html",
        visit=visit,
        patient=patient,
        products=Product.query.filter_by(is_active=True).order_by(Product.name).all(),
    )


@pharmacy_bp.route("/<int:prescription_id>")
@login_required
def view_prescription(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    return render_template("pharmacy/view.html", prescription=prescription)


@pharmacy_bp.route("/items/<int:item_id>/dispense", methods=["POST"])
@login_required
def dispense_item(item_id):
    item = PrescriptionItem.query.get_or_404(item_id)
    product = item.product

    if product and product.quantity_in_stock < item.quantity:
        flash(f"Not enough stock of {product.name} — only {product.quantity_in_stock} left.", "error")
        return redirect(url_for("pharmacy.view_prescription", prescription_id=item.prescription_id))

    item.has_been_dispensed = True
    item.dispensed_at = datetime.now(timezone.utc)
    if product:
        product.quantity_in_stock -= item.quantity
        db.session.add(StockMovement(
            product_id=product.product_id,
            quantity_change=-item.quantity,
            reason=f"Dispensed — prescription #{item.prescription_id}",
            recorded_by=current_user.system_user_id,
        ))

    visit = item.prescription.visit
    billed_note = ""
    if visit and product:
        bill = MedicalBill.get_or_create_for_visit(visit)
        bill.add_item(
            name=f"{product.name} x{item.quantity}",
            quantity=1,
            rate=product.unit_price * item.quantity,
        )
        db.session.commit()
        billed_note = f" Added to bill {bill.medical_bill_no}."
    else:
        db.session.commit()

    flash(f"{item.inscription} dispensed.{billed_note}", "success")
    return redirect(url_for("pharmacy.view_prescription", prescription_id=item.prescription_id))


# ── Product catalog (simple admin) ──────────────────────────────────────

@pharmacy_bp.route("/products")
@login_required
def list_products():
    products = Product.query.order_by(Product.name).all()
    return render_template("pharmacy/products.html", products=products)


@pharmacy_bp.route("/products/<int:product_id>/receive", methods=["GET", "POST"])
@login_required
def receive_stock(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        qty = int(request.form.get("quantity", "0") or "0")
        if qty <= 0:
            flash("Enter a quantity greater than zero.", "error")
            return redirect(url_for("pharmacy.receive_stock", product_id=product.product_id))

        supplier = Supplier.query.get(request.form.get("supplier_id")) if request.form.get("supplier_id") else None
        note = request.form.get("note", "").strip()

        reason_parts = ["Stock intake"]
        if supplier:
            reason_parts.append(f"from {supplier.name}")
        if note:
            reason_parts.append(f"— {note}")
        reason = " ".join(reason_parts)

        product.quantity_in_stock += qty
        db.session.add(StockMovement(
            product_id=product.product_id,
            supplier_id=supplier.supplier_id if supplier else None,
            quantity_change=qty,
            reason=reason,
            recorded_by=current_user.system_user_id,
        ))
        db.session.commit()
        flash(f"Received {qty} x {product.name} — now {product.quantity_in_stock} in stock.", "success")
        return redirect(url_for("pharmacy.list_products"))

    return render_template(
        "pharmacy/receive_stock.html",
        product=product,
        suppliers=Supplier.query.filter_by(is_active=True).order_by(Supplier.name).all(),
    )


# ── Suppliers (simple admin) ────────────────────────────────────────────

@pharmacy_bp.route("/suppliers")
@login_required
def list_suppliers():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return render_template("pharmacy/suppliers.html", suppliers=suppliers)


@pharmacy_bp.route("/suppliers/<int:supplier_id>/edit", methods=["GET", "POST"])
@login_required
def edit_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)

    if request.method == "POST":
        supplier.name = request.form["name"].strip()
        supplier.contact_person = request.form.get("contact_person") or None
        supplier.telephone = request.form.get("telephone") or None
        supplier.email = request.form.get("email") or None
        supplier.is_active = bool(request.form.get("is_active"))
        db.session.commit()
        flash(f"Supplier '{supplier.name}' updated.", "success")
        return redirect(url_for("pharmacy.list_suppliers"))

    return render_template("pharmacy/supplier_form.html", supplier=supplier)


@pharmacy_bp.route("/suppliers/new", methods=["GET", "POST"])
@login_required
def new_supplier():
    if request.method == "POST":
        supplier = Supplier(
            name=request.form["name"].strip(),
            contact_person=request.form.get("contact_person") or None,
            telephone=request.form.get("telephone") or None,
            email=request.form.get("email") or None,
        )
        db.session.add(supplier)
        db.session.commit()
        flash(f"Supplier '{supplier.name}' added.", "success")

        next_url = request.args.get("next")
        return redirect(next_url or url_for("pharmacy.list_suppliers"))
    return render_template("pharmacy/supplier_form.html")


@pharmacy_bp.route("/products/<int:product_id>/history")
@login_required
def stock_history(product_id):
    product = Product.query.get_or_404(product_id)
    movements = (
        StockMovement.query
        .filter_by(product_id=product.product_id)
        .order_by(StockMovement.created_at.desc())
        .limit(100)
        .all()
    )
    return render_template("pharmacy/stock_history.html", product=product, movements=movements)


@pharmacy_bp.route("/products/new", methods=["GET", "POST"])
@login_required
def new_product():
    if request.method == "POST":
        product = Product(
            name=request.form["name"].strip(),
            code=request.form.get("code") or None,
            unit_definition=request.form.get("unit_definition") or None,
            unit_cost=Decimal(request.form.get("unit_cost", "0") or "0"),
            unit_price=Decimal(request.form.get("unit_price", "0") or "0"),
            quantity_in_stock=int(request.form.get("quantity_in_stock", "0") or "0"),
            reorder_level=int(request.form.get("reorder_level", "0") or "0"),
        )
        db.session.add(product)
        db.session.commit()
        flash(f"Product '{product.name}' added.", "success")
        return redirect(url_for("pharmacy.list_products"))
    return render_template("pharmacy/product_form.html")
