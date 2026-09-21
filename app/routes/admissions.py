from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Admission, AdmissionWard, Patient, Visit, Ward, Bed

admissions_bp = Blueprint("admissions", __name__, url_prefix="/admissions")


@admissions_bp.route("/")
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
            admitting_doctor=request.form.get("admitting_doctor") or None,
            received_by_nurse=request.form.get("received_by_nurse") or None,
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
        return redirect(url_for("admissions.list_admissions"))

    return render_template(
        "admissions/new.html",
        visit=visit,
        patient=patient,
        available_beds=Bed.query.filter_by(bed_status="Vacant").order_by(Bed.ward_id, Bed.bed_no).all(),
    )


@admissions_bp.route("/<int:admission_id>/discharge", methods=["POST"])
def discharge(admission_id):
    admission = Admission.query.get_or_404(admission_id)
    admission.is_in_admission = False
    admission.discharge_datetime = datetime.now(timezone.utc)
    admission.discharging_doctor = request.form.get("discharging_doctor") or None

    current = admission.current_bed_assignment
    if current:
        current.is_current_bed = False
        current.bed.bed_status = "Vacant"

    db.session.commit()
    flash(f"{admission.patient.full_name} discharged.", "success")
    return redirect(url_for("admissions.list_admissions"))


# ── Wards & Beds (simple admin) ─────────────────────────────────────────

@admissions_bp.route("/wards")
def list_wards():
    wards = Ward.query.order_by(Ward.name).all()
    return render_template("admissions/wards.html", wards=wards)


@admissions_bp.route("/wards/new", methods=["GET", "POST"])
def new_ward():
    if request.method == "POST":
        ward = Ward(name=request.form["name"].strip())
        db.session.add(ward)
        db.session.commit()
        flash(f"Ward '{ward.name}' added.", "success")
        return redirect(url_for("admissions.list_wards"))
    return render_template("admissions/ward_form.html")


@admissions_bp.route("/wards/<int:ward_id>/beds/new", methods=["GET", "POST"])
def new_bed(ward_id):
    ward = Ward.query.get_or_404(ward_id)
    if request.method == "POST":
        bed = Bed(ward_id=ward.ward_id, bed_no=request.form["bed_no"].strip())
        db.session.add(bed)
        db.session.commit()
        flash(f"Bed '{bed.bed_no}' added to {ward.name}.", "success")
        return redirect(url_for("admissions.list_wards"))
    return render_template("admissions/bed_form.html", ward=ward)
