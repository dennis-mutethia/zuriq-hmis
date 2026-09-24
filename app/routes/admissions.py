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
        db.session.flush()  # need admission_id before the bed assignment row

        if bed:
            db.session.add(AdmissionWard(
                admission_id=admission.admission_id,
                ward_id=bed.ward_id,
                bed_id=bed.bed_id,
                is_current_bed=True,
            ))
            bed.bed_status = "Occupied"

        visit.is_admitted = True
        db.session.commit()
        # in_patient_no is assigned by a DB trigger right after insert;
        # commit() expires the object so the next access re-fetches it.
        flash(f"{patient.full_name} admitted — IP number {patient.in_patient_no}.", "success")
        next_url = request.args.get("next")
        return redirect(next_url or url_for("admissions.list_admissions"))

    return render_template(
        "admissions/new.html",
        visit=visit,
        patient=patient,
        default_doctor=current_user.username,
        available_beds=Bed.query.filter_by(bed_status="Vacant").order_by(Bed.ward_id, Bed.bed_no).all(),
    )


@admissions_bp.route("/<int:admission_id>/discharge", methods=["GET", "POST"])
@login_required
def discharge(admission_id):
    admission = Admission.query.get_or_404(admission_id)

    if request.method == "POST":
        outcome = request.form.get("discharge_outcome")
        if outcome not in ("Alive", "Deceased", "Referred", "Discharged Against Medical Advice"):
            flash("Select a discharge outcome.", "error")
            return redirect(url_for("admissions.discharge", admission_id=admission.admission_id))

        admission.is_in_admission = False
        admission.discharge_datetime = datetime.now(timezone.utc)
        admission.discharging_doctor = request.form.get("discharging_doctor") or None
        admission.discharge_outcome = outcome
        admission.discharge_diagnosis = request.form.get("discharge_diagnosis") or None
        admission.discharge_notes = request.form.get("discharge_notes") or None
        admission.discharge_medication = request.form.get("discharge_medication") or None
        admission.discharged_by = current_user.system_user_id

        current = admission.current_bed_assignment
        if current:
            current.is_current_bed = False
            current.bed.bed_status = "Vacant"

        db.session.commit()
        flash(f"{admission.patient.full_name} discharged.", "success")
        return redirect(url_for("admissions.discharge_summary", admission_id=admission.admission_id))

    # Discharging doctor auto-picks the logged-in user, same as
    # Consultation — never overwrites a value someone already entered.
    if not admission.discharging_doctor:
        admission.discharging_doctor = current_user.username

    return render_template("admissions/discharge.html", admission=admission)


@admissions_bp.route("/<int:admission_id>/discharge-summary")
@login_required
def discharge_summary(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    visit = admission.visit
    lab_requests = (
        LabRequest.query.filter_by(visit_id=visit.visit_id).order_by(LabRequest.date_time_requested).all()
        if visit else []
    )
    prescriptions = (
        Prescription.query.filter_by(visit_id=visit.visit_id).order_by(Prescription.created_at).all()
        if visit else []
    )
    return render_template(
        "admissions/discharge_summary.html",
        admission=admission, visit=visit, lab_requests=lab_requests, prescriptions=prescriptions,
    )


# ── Wards & Beds (simple admin) ─────────────────────────────────────────

@admissions_bp.route("/wards")
@login_required
def list_wards():
    wards = Ward.query.order_by(Ward.name).all()
    return render_template("admissions/wards.html", wards=wards)


@admissions_bp.route("/wards/new", methods=["GET", "POST"])
@login_required
def new_ward():
    if request.method == "POST":
        ward = Ward(name=request.form["name"].strip())
        db.session.add(ward)
        db.session.commit()
        flash(f"Ward '{ward.name}' added.", "success")
        return redirect(url_for("admissions.list_wards"))
    return render_template("admissions/ward_form.html")


@admissions_bp.route("/wards/<int:ward_id>/beds/new", methods=["GET", "POST"])
@login_required
def new_bed(ward_id):
    ward = Ward.query.get_or_404(ward_id)
    if request.method == "POST":
        bed = Bed(ward_id=ward.ward_id, bed_no=request.form["bed_no"].strip())
        db.session.add(bed)
        db.session.commit()
        flash(f"Bed '{bed.bed_no}' added to {ward.name}.", "success")
        return redirect(url_for("admissions.list_wards"))
    return render_template("admissions/bed_form.html", ward=ward)
