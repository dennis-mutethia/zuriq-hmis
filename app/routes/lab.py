from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import LabRequest, LabRequestItem, Test, Visit

lab_bp = Blueprint("lab", __name__, url_prefix="/lab")


@lab_bp.route("/")
@login_required
def list_requests():
    status = request.args.get("status", "pending")
    query = LabRequest.query
    if status == "pending":
        query = query.filter_by(is_done=False)
    elif status == "done":
        query = query.filter_by(is_done=True)
    requests_ = query.order_by(LabRequest.date_time_requested.desc()).limit(200).all()
    return render_template("lab/list.html", requests=requests_, status=status)


@lab_bp.route("/visit/<int:visit_id>/new", methods=["GET", "POST"])
@login_required
def new_request(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    patient = visit.patient

    if request.method == "POST":
        test_ids = request.form.getlist("test_id")
        if not test_ids:
            flash("Select at least one test before saving.", "error")
            return redirect(url_for("lab.new_request", visit_id=visit.visit_id))

        lab_request = LabRequest(
            visit_id=visit.visit_id,
            patient_id=patient.patient_id,
        )
        db.session.add(lab_request)
        db.session.flush()

        for test_id in test_ids:
            test = Test.query.get(test_id)
            if not test:
                continue
            db.session.add(LabRequestItem(
                lab_request_id=lab_request.lab_request_id,
                test_id=test.test_id,
                test_name=test.name,
            ))

        db.session.commit()
        flash(f"Lab request created for {patient.full_name}.", "success")
        return redirect(url_for("lab.list_requests"))

    return render_template(
        "lab/new.html",
        visit=visit,
        patient=patient,
        tests=Test.query.filter_by(is_active=True).order_by(Test.name).all(),
    )


@lab_bp.route("/<int:lab_request_id>", methods=["GET", "POST"])
@login_required
def view_request(lab_request_id):
    lab_request = LabRequest.query.get_or_404(lab_request_id)

    if request.method == "POST":
        for item in lab_request.items:
            field = f"conclusion_{item.lab_request_item_id}"
            item.conclusion = request.form.get(field) or None

        lab_request.technologist = request.form.get("technologist") or None
        lab_request.is_done = True
        lab_request.date_time_done = datetime.now(timezone.utc)
        db.session.commit()
        flash("Results saved.", "success")
        return redirect(url_for("lab.list_requests"))

    return render_template("lab/view.html", lab_request=lab_request)


# ── Test catalog (simple admin) ─────────────────────────────────────────

@lab_bp.route("/tests")
@login_required
def list_tests():
    tests = Test.query.order_by(Test.name).all()
    return render_template("lab/tests.html", tests=tests)


@lab_bp.route("/tests/new", methods=["GET", "POST"])
@login_required
def new_test():
    if request.method == "POST":
        test = Test(
            name=request.form["name"].strip(),
            specimen=request.form.get("specimen") or None,
        )
        db.session.add(test)
        db.session.commit()
        flash(f"Test '{test.name}' added.", "success")
        return redirect(url_for("lab.list_tests"))
    return render_template("lab/test_form.html")
