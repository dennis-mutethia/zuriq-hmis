from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Visit, Patient, Clinic

visits_bp = Blueprint("visits", __name__, url_prefix="/visits")


def _calc_age(dob):
    if not dob:
        return None, None, None
    today = date.today()
    dob_date = dob.date() if hasattr(dob, "date") else dob
    years = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    if years >= 5:
        return years, None, None
    months = (today.year - dob_date.year) * 12 + (today.month - dob_date.month)
    if months >= 1:
        return years, months, None
    weeks = (today - dob_date).days // 7
    return years, months, weeks


@visits_bp.route("/")
@login_required
def list_visits():
    q = request.args.get("q", "").strip()
    query = Visit.query.join(Patient)
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(
                Patient.surname.ilike(like),
                Patient.other_names.ilike(like),
                Patient.out_patient_no.ilike(like),
            )
        )
    visits = query.order_by(Visit.visit_datetime.desc()).limit(200).all()
    return render_template("visits/list.html", visits=visits, q=q)


@visits_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_visit():
    patient = None
    patient_id = request.values.get("patient_id")
    if patient_id:
        patient = Patient.query.get_or_404(patient_id)

    if request.method == "POST":
        patient = Patient.query.get_or_404(request.form["patient_id"])
        age, age_months, age_weeks = _calc_age(patient.date_of_birth)

        visit = Visit(
            patient_id=patient.patient_id,
            clinic_id=request.form.get("clinic_id") or None,
            age=age,
            age_months=age_months,
            age_weeks=age_weeks,
            doctor=request.form.get("doctor") or None,
            nurse=request.form.get("nurse") or None,
            hpi=request.form.get("hpi") or None,
            is_consultant=bool(request.form.get("is_consultant")),
        )
        db.session.add(visit)
        db.session.commit()
        flash(f"Visit recorded for {patient.full_name}.", "success")
        return redirect(url_for("visits.list_visits"))

    return render_template(
        "visits/form.html",
        patient=patient,
        clinics=Clinic.query.order_by(Clinic.name).all(),
    )


@visits_bp.route("/find-patient")
@login_required
def find_patient():
    """Small helper endpoint: search patients to attach a new visit to."""
    q = request.args.get("q", "").strip()
    patients = []
    if q:
        like = f"%{q}%"
        patients = Patient.query.filter(
            db.or_(
                Patient.surname.ilike(like),
                Patient.other_names.ilike(like),
                Patient.out_patient_no.ilike(like),
            )
        ).limit(20).all()
    return render_template("visits/find_patient.html", patients=patients, q=q)
