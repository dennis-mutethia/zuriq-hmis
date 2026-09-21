from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import SystemUser

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = SystemUser.query.filter_by(username=username).first()

        if user and user.is_active and user.check_password(password):
            login_user(user)
            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard.home"))

        flash("Incorrect username or password.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


# ── Staff accounts ───────────────────────────────────────────────────────
# No roles/permissions yet — any logged-in user can create another account.
# Fine for a small team; worth adding an admin-only check before this goes
# out to a larger staff list.

@auth_bp.route("/users")
@login_required
def list_users():
    users = SystemUser.query.order_by(SystemUser.username).all()
    return render_template("auth/users.html", users=users)


@auth_bp.route("/users/new", methods=["GET", "POST"])
@login_required
def new_user():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if SystemUser.query.filter_by(username=username).first():
            flash(f"A user named '{username}' already exists.", "error")
            return redirect(url_for("auth.new_user"))

        user = SystemUser(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash(f"User '{username}' created.", "success")
        return redirect(url_for("auth.list_users"))

    return render_template("auth/user_form.html")
