from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Consultant, ConsultantBooking, Patient

consultants_bp = Blueprint("consultants", __name__, url_prefix="/consultants")


@consultants_bp.route("/")
@login_required
def list_consultants():
    consultants = Consultant.query.filter_by(is_active=True).order_by(Consultant.surname).all()
    patient = None
    patient_id = request.args.get("patient_id")
    if patient_id:
        patient = Patient.query.get(patient_id)
    return render_template("consultants/list.html", consultants=consultants, patient=patient)


@consultants_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_consultant():
    if request.method == "POST":
        consultant = Consultant(
            surname=request.form["surname"].strip(),
            other_names=request.form["other_names"].strip(),
            alias=request.form.get("alias") or None,
            designation=request.form.get("designation") or None,
            mobile_no=request.form.get("mobile_no") or None,
        )
        db.session.add(consultant)
        db.session.commit()
        flash(f"Consultant {consultant.full_name} added.", "success")
        return redirect(url_for("consultants.list_consultants"))
    return render_template("consultants/form.html", consultant=None)


@consultants_bp.route("/<int:consultant_id>/edit", methods=["GET", "POST"])
@login_required
def edit_consultant(consultant_id):
    consultant = Consultant.query.get_or_404(consultant_id)
    if request.method == "POST":
        consultant.surname = request.form["surname"].strip()
        consultant.other_names = request.form["other_names"].strip()
        consultant.alias = request.form.get("alias") or None
        consultant.designation = request.form.get("designation") or None
        consultant.mobile_no = request.form.get("mobile_no") or None
        consultant.is_active = bool(request.form.get("is_active"))
        db.session.commit()
        flash(f"Consultant {consultant.full_name} updated.", "success")
        return redirect(url_for("consultants.list_consultants"))
    return render_template("consultants/form.html", consultant=consultant)


@consultants_bp.route("/<int:consultant_id>/bookings")
@login_required
def view_bookings(consultant_id):
    consultant = Consultant.query.get_or_404(consultant_id)
    bookings = (
        ConsultantBooking.query
        .filter_by(consultant_id=consultant.consultant_id)
        .order_by(ConsultantBooking.visit_datetime.desc().nullslast(), ConsultantBooking.datetime_booked.desc())
        .all()
    )
    return render_template("consultants/bookings.html", consultant=consultant, bookings=bookings)


@consultants_bp.route("/<int:consultant_id>/book", methods=["GET", "POST"])
@login_required
def new_booking(consultant_id):
    consultant = Consultant.query.get_or_404(consultant_id)

    if request.method == "POST":
        patient = Patient.query.get_or_404(request.form["patient_id"])
        booking = ConsultantBooking(
            consultant_id=consultant.consultant_id,
            patient_id=patient.patient_id,
            visit_datetime=request.form.get("visit_datetime") or None,
            booked_by=current_user.system_user_id,
        )
        db.session.add(booking)
        db.session.commit()
        flash(f"Booked {patient.full_name} with {consultant.display_name}.", "success")
        return redirect(url_for("consultants.view_bookings", consultant_id=consultant.consultant_id))

    # If a patient_id was passed in (e.g. from Admissions' "See Specialist"
    # link), skip the search step and go straight to confirming the booking.
    preselected_patient = None
    preselected_id = request.values.get("patient_id")
    if preselected_id:
        preselected_patient = Patient.query.get(preselected_id)

    q = request.args.get("q", "").strip()
    patients = []
    if q:
        like = f"%{q}%"
        patients = Patient.query.filter(
            db.or_(Patient.surname.ilike(like), Patient.other_names.ilike(like), Patient.out_patient_no.ilike(like))
        ).limit(20).all()
    return render_template(
        "consultants/book.html",
        consultant=consultant, patients=patients, q=q, preselected_patient=preselected_patient,
    )


@consultants_bp.route("/bookings/<int:consultant_booking_id>/seen", methods=["POST"])
@login_required
def mark_seen(consultant_booking_id):
    booking = ConsultantBooking.query.get_or_404(consultant_booking_id)
    booking.is_seen = True
    db.session.commit()
    flash(f"{booking.patient.full_name} marked as seen.", "success")
    return redirect(url_for("consultants.view_bookings", consultant_id=booking.consultant_id))
