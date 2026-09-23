from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import NurseTriage, ObservationChart, Visit, Admission, QueueEntry

nursing_bp = Blueprint("nursing", __name__, url_prefix="/nursing")


def _dec(val):
    if val in (None, ""):
        return None
    try:
        return Decimal(val)
    except InvalidOperation:
        return None


@nursing_bp.route("/")
@login_required
def list_triage():
    records = NurseTriage.query.order_by(NurseTriage.created_at.desc()).limit(200).all()
    queue_entries = QueueEntry.for_room_function("triage")
    return render_template("nursing/list.html", records=records, queue_entries=queue_entries)


@nursing_bp.route("/visit/<int:visit_id>/triage", methods=["GET", "POST"])
@login_required
def new_triage(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    patient = visit.patient

    if request.method == "POST":
        triage = NurseTriage(
            visit_id=visit.visit_id,
            blood_pressure=request.form.get("blood_pressure") or None,
            blood_pressure_remarks=request.form.get("blood_pressure_remarks") or None,
            pulse_rate=_dec(request.form.get("pulse_rate")),
            pulse_rate_remarks=request.form.get("pulse_rate_remarks") or None,
            respiration_rate=_dec(request.form.get("respiration_rate")),
            respiration_rate_remarks=request.form.get("respiration_rate_remarks") or None,
            temperature=_dec(request.form.get("temperature")),
            temperature_remarks=request.form.get("temperature_remarks") or None,
            weight=_dec(request.form.get("weight")),
            weight_remarks=request.form.get("weight_remarks") or None,
            notes=request.form.get("notes") or None,
            recorded_by=current_user.system_user_id,
        )
        db.session.add(triage)
        QueueEntry.complete_for_visit(visit.visit_id)
        db.session.commit()
        flash(f"Triage recorded for {patient.full_name}.", "success")
        return redirect(url_for("nursing.list_triage"))

    return render_template("nursing/triage_form.html", visit=visit, patient=patient)


@nursing_bp.route("/admission/<int:admission_id>", methods=["GET", "POST"])
@login_required
def observation_chart(admission_id):
    admission = Admission.query.get_or_404(admission_id)

    if request.method == "POST":
        obs = ObservationChart(
            admission_id=admission.admission_id,
            systolic=_dec(request.form.get("systolic")),
            diastolic=_dec(request.form.get("diastolic")),
            pulse=_dec(request.form.get("pulse")),
            respiratory=_dec(request.form.get("respiratory")),
            spo2=_dec(request.form.get("spo2")),
            temperature=_dec(request.form.get("temperature")),
            comments=request.form.get("comments") or None,
            recorded_by=current_user.system_user_id,
        )
        db.session.add(obs)
        db.session.commit()
        flash(f"Observation recorded for {admission.patient.full_name}.", "success")
        return redirect(url_for("nursing.observation_chart", admission_id=admission.admission_id))

    readings = ObservationChart.query.filter_by(admission_id=admission.admission_id).order_by(ObservationChart.created_at.desc()).all()
    return render_template("nursing/observation_chart.html", admission=admission, readings=readings)
