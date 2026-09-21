from datetime import datetime, timezone
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Prescription, PrescriptionItem, Product, Visit

pharmacy_bp = Blueprint("pharmacy", __name__, url_prefix="/pharmacy")


@pharmacy_bp.route("/")
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
        return redirect(url_for("pharmacy.list_prescriptions"))

    return render_template(
        "pharmacy/new.html",
        visit=visit,
        patient=patient,
        products=Product.query.filter_by(is_active=True).order_by(Product.name).all(),
    )


@pharmacy_bp.route("/<int:prescription_id>")
def view_prescription(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    return render_template("pharmacy/view.html", prescription=prescription)


@pharmacy_bp.route("/items/<int:item_id>/dispense", methods=["POST"])
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

    db.session.commit()
    flash(f"{item.inscription} dispensed.", "success")
    return redirect(url_for("pharmacy.view_prescription", prescription_id=item.prescription_id))


# ── Product catalog (simple admin) ──────────────────────────────────────

@pharmacy_bp.route("/products")
def list_products():
    products = Product.query.order_by(Product.name).all()
    return render_template("pharmacy/products.html", products=products)


@pharmacy_bp.route("/products/new", methods=["GET", "POST"])
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
