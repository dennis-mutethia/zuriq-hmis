from datetime import date, timedelta
from flask import Blueprint, render_template
from flask_login import login_required
from app import db
from app.models import MedicalBill, Visit, Product

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/")
@login_required
def home():
    # Revenue collected per day, last 30 days
    revenue_since = date.today() - timedelta(days=29)
    revenue_rows = (
        db.session.query(
            db.func.date(MedicalBill.date_time_created).label("day"),
            db.func.coalesce(db.func.sum(MedicalBill.total_amount_paid), 0).label("total"),
        )
        .filter(db.func.date(MedicalBill.date_time_created) >= revenue_since)
        .group_by("day")
        .order_by("day")
        .all()
    )
    revenue_labels = [r.day.strftime("%d %b") for r in revenue_rows]
    revenue_values = [float(r.total) for r in revenue_rows]

    # Visit volume per day, last 14 days
    visits_since = date.today() - timedelta(days=13)
    visit_rows = (
        db.session.query(
            db.func.date(Visit.visit_datetime).label("day"),
            db.func.count(Visit.visit_id).label("count"),
        )
        .filter(db.func.date(Visit.visit_datetime) >= visits_since)
        .group_by("day")
        .order_by("day")
        .all()
    )
    visit_labels = [r.day.strftime("%d %b") for r in visit_rows]
    visit_values = [r.count for r in visit_rows]

    # Outstanding bills — computed in Python since balance_due isn't a DB column
    all_pending = MedicalBill.query.filter_by(is_processed=False).all()
    total_outstanding = sum((b.balance_due for b in all_pending), start=0)
    top_outstanding = sorted(all_pending, key=lambda b: b.balance_due, reverse=True)[:10]

    low_stock = (
        Product.query
        .filter(Product.is_active.is_(True), Product.quantity_in_stock <= Product.reorder_level)
        .order_by(Product.quantity_in_stock)
        .all()
    )

    return render_template(
        "reports/index.html",
        revenue_labels=revenue_labels,
        revenue_values=revenue_values,
        visit_labels=visit_labels,
        visit_values=visit_values,
        total_outstanding=total_outstanding,
        top_outstanding=top_outstanding,
        low_stock=low_stock,
    )
