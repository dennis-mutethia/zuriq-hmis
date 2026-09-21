from datetime import date, datetime, timezone
from flask import Blueprint, render_template
from app import db
from app.models import Patient, Visit, MedicalBill

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
    today_start = datetime.combine(date.today(), datetime.min.time(), tzinfo=timezone.utc)

    stats = {
        "total_patients": Patient.query.count(),
        "visits_today": Visit.query.filter(Visit.visit_datetime >= today_start).count(),
        "pending_bills": MedicalBill.query.filter_by(is_processed=False).count(),
        "collected_today": db.session.query(
            db.func.coalesce(db.func.sum(MedicalBill.total_amount_paid), 0)
        ).filter(MedicalBill.date_time_created >= today_start).scalar(),
    }
    recent_visits = Visit.query.order_by(Visit.visit_datetime.desc()).limit(6).all()

    return render_template("dashboard.html", stats=stats, recent_visits=recent_visits)
