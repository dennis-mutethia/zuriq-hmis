from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Admission, AdmissionWard, Patient, Visit, Ward, Bed, LabRequest, Prescription

admissions_bp = Blueprint("admissions", __name__, url_prefix="/admissions")


@admissions_bp.route("/")
@login_required
def list_admissions():
    status = request.args.get("status", "current")
    query = Admission.query
    if status == "current":
        query = query.filter_by(is_in_admission=True)
    elif status == "discharged":
        query = query.filter_by(is_in_admission=False)
    admissions = query.order_by(Admission.admission_datetime.desc()).limit(200).all()
    return render_template("admissions/list.html", admissions=admissions, status=status)


@admissions_bp.route("/visit/<int:visit_id>/new", methods=["GET", "POST"])
@login_required
def new_admission(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    patient = visit.patient

    if request.method == "POST":
        bed_id = request.form.get("bed_id")
        bed = Bed.query.get_or_404(bed_id) if bed_id else None
        if bed and bed.bed_status == "Occupied":
            flash("That bed is already occupied — pick another.", "error")
            return redirect(url_for("admissions.new_admission", visit_id=visit.visit_id))

        admission = Admission(
            visit_id=visit.visit_id,
            patient_id=patient.patient_id,
            admitted_by=current_user.system_user_id,
            admitting_doctor=request.form.get("admitting_doctor") or None,
            received_by_nurse=request.form.get("received_by_nurse") or None,
            admission_diagnosis=request.form.get("admission_diagnosis") or None,
        )
        db.session.add(admission)