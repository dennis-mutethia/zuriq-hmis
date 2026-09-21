from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Patient, IdType, Nationality, GroupAccount

patients_bp = Blueprint("patients", __name__, url_prefix="/patients")


@patients_bp.route("/")
@login_required
def list_patients():
    q = request.args.get("q", "").strip()
    query = Patient.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(
                Patient.surname.ilike(like),
                Patient.other_names.ilike(like),
                Patient.out_patient_no.cast(db.String).ilike(like),
                Patient.id_number.ilike(like),
            )
        )
    patients = query.order_by(Patient.date_registered.desc()).limit(200).all()
    return render_template("patients/list.html", patients=patients, q=q)


@patients_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_patient():
    if request.method == "POST":
        patient = Patient(
            surname=request.form["surname"].strip(),
            other_names=request.form["other_names"].strip(),
            third_name=request.form.get("third_name", "").strip() or None,
            sex=request.form["sex"],
            date_of_birth=request.form.get("date_of_birth") or None,
            occupation=request.form.get("occupation") or None,
            residence=request.form.get("residence") or None,
            city_town=request.form.get("city_town") or None,
            telephone1=request.form.get("telephone1") or None,
            telephone2=request.form.get("telephone2") or None,
            email_address=request.form.get("email_address") or None,
            postal_address=request.form.get("postal_address") or None,
            postal_code=request.form.get("postal_code") or None,
            next_of_kin=request.form.get("next_of_kin") or None,
            next_of_kin_relationship=request.form.get("next_of_kin_relationship") or None,
            next_of_kin_contact=request.form.get("next_of_kin_contact") or None,
            id_type_id=request.form.get("id_type_id") or None,
            id_number=request.form.get("id_number") or None,
            nationality_id=request.form.get("nationality_id") or None,
            group_account_id=request.form.get("group_account_id") or None,
            reference_no=request.form.get("reference_no") or None,
            note=request.form.get("note") or None,
        )
        db.session.add(patient)
        db.session.commit()
        # out_patient_no/in_patient_no are filled in by a DB trigger right
        # after insert; commit() expires the object so this access re-fetches
        # the row and picks up the generated values.
        flash(f"Patient {patient.full_name} registered — OP number {patient.out_patient_no}.", "success")
        return redirect(url_for("patients.list_patients"))

    return render_template(
        "patients/form.html",
        patient=None,
        id_types=IdType.query.all(),
        nationalities=Nationality.query.all(),
        group_accounts=GroupAccount.query.filter_by(is_active=True).all(),
    )


@patients_bp.route("/<int:patient_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if request.method == "POST":
        for field in [
            "surname", "other_names", "third_name", "sex", "occupation",
            "residence", "city_town", "telephone1", "telephone2", "email_address",
            "postal_address", "postal_code", "next_of_kin", "next_of_kin_relationship",
            "next_of_kin_contact", "id_number", "reference_no", "note",
        ]:
            setattr(patient, field, request.form.get(field) or None)

        patient.date_of_birth = request.form.get("date_of_birth") or None
        patient.id_type_id = request.form.get("id_type_id") or None
        patient.nationality_id = request.form.get("nationality_id") or None
        patient.group_account_id = request.form.get("group_account_id") or None
        patient.out_patient_no = request.form.get("out_patient_no") or None

        db.session.commit()
        flash(f"Patient {patient.full_name} updated.", "success")
        return redirect(url_for("patients.list_patients"))

    return render_template(
        "patients/form.html",
        patient=patient,
        id_types=IdType.query.all(),
        nationalities=Nationality.query.all(),
        group_accounts=GroupAccount.query.filter_by(is_active=True).all(),
    )


@patients_bp.route("/<int:patient_id>/delete", methods=["POST"])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash("Patient record deleted.", "info")
    return redirect(url_for("patients.list_patients"))
