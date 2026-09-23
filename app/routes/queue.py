from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import QueueEntry, Room, Visit

queue_bp = Blueprint("queue", __name__, url_prefix="/queue")


@queue_bp.route("/")
@login_required
def board():
    rooms = Room.query.order_by(Room.room_id).all()
    active = (
        QueueEntry.query
        .filter(QueueEntry.completed_at.is_(None))
        .order_by(QueueEntry.queued_at)
        .all()
    )
    by_room = {r.room_id: [] for r in rooms}
    for entry in active:
        by_room.setdefault(entry.to_room_id, []).append(entry)

    return render_template("queue/board.html", rooms=rooms, by_room=by_room)


@queue_bp.route("/visit/<int:visit_id>/join", methods=["GET", "POST"])
@login_required
def join(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    patient = visit.patient

    if request.method == "POST":
        to_room_id = request.form.get("to_room_id")
        if not to_room_id:
            flash("Pick a room to queue for.", "error")
            return redirect(url_for("queue.join", visit_id=visit.visit_id))

        # If they're already waiting somewhere else, that's their "from" room
        last_entry = (
            QueueEntry.query
            .filter_by(visit_id=visit.visit_id)
            .order_by(QueueEntry.queued_at.desc())
            .first()
        )
        from_room_id = last_entry.to_room_id if last_entry else None

        entry = QueueEntry(
            visit_id=visit.visit_id,
            from_room_id=from_room_id,
            to_room_id=to_room_id,
            created_by=current_user.system_user_id,
        )
        db.session.add(entry)
        db.session.commit()
        flash(f"{patient.full_name} added to the {entry.to_room.name} queue.", "success")
        return redirect(url_for("queue.board"))

    return render_template("queue/join.html", visit=visit, patient=patient, rooms=Room.query.order_by(Room.room_id).all())


@queue_bp.route("/<int:queue_entry_id>/call", methods=["POST"])
@login_required
def call(queue_entry_id):
    entry = QueueEntry.query.get_or_404(queue_entry_id)
    entry.called_at = datetime.now(timezone.utc)
    db.session.commit()
    flash(f"{entry.visit.patient.full_name} called into {entry.to_room.name}.", "success")
    return redirect(request.form.get("next") or url_for("queue.board"))


@queue_bp.route("/<int:queue_entry_id>/complete", methods=["POST"])
@login_required
def complete(queue_entry_id):
    entry = QueueEntry.query.get_or_404(queue_entry_id)
    if not entry.called_at:
        entry.called_at = datetime.now(timezone.utc)
    entry.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    flash(f"{entry.visit.patient.full_name} done at {entry.to_room.name}.", "success")
    return redirect(request.form.get("next") or url_for("queue.board"))


# ── Rooms (simple admin) ─────────────────────────────────────────────────

@queue_bp.route("/rooms")
@login_required
def list_rooms():
    rooms = Room.query.order_by(Room.room_id).all()
    return render_template("queue/rooms.html", rooms=rooms)


@queue_bp.route("/rooms/new", methods=["GET", "POST"])
@login_required
def new_room():
    if request.method == "POST":
        name = request.form["name"].strip()
        if Room.query.filter_by(name=name).first():
            flash(f"A room named '{name}' already exists.", "error")
            return redirect(url_for("queue.new_room"))
        db.session.add(Room(name=name, function=request.form.get("function") or None))
        db.session.commit()
        flash(f"Room '{name}' added.", "success")
        return redirect(url_for("queue.list_rooms"))
    return render_template("queue/room_form.html", room=None)


@queue_bp.route("/rooms/<int:room_id>/edit", methods=["GET", "POST"])
@login_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == "POST":
        room.name = request.form["name"].strip()
        room.function = request.form.get("function") or None
        db.session.commit()
        flash(f"Room '{room.name}' updated.", "success")
        return redirect(url_for("queue.list_rooms"))
    return render_template("queue/room_form.html", room=room)
