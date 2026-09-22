from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import SystemUser
        return SystemUser.query.get(int(user_id))

    from app.nav import nav_link
    app.jinja_env.globals["nav_link"] = nav_link

    from app.cli import register_cli
    register_cli(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.patients import patients_bp
    app.register_blueprint(patients_bp)

    from app.routes.visits import visits_bp
    app.register_blueprint(visits_bp)

    from app.routes.queue import queue_bp
    app.register_blueprint(queue_bp)

    from app.routes.nursing import nursing_bp
    app.register_blueprint(nursing_bp)

    from app.routes.billing import billing_bp
    app.register_blueprint(billing_bp)

    from app.routes.accounts import accounts_bp
    app.register_blueprint(accounts_bp)

    from app.routes.hr import hr_bp
    app.register_blueprint(hr_bp)

    from app.routes.admissions import admissions_bp
    app.register_blueprint(admissions_bp)

    from app.routes.pharmacy import pharmacy_bp
    app.register_blueprint(pharmacy_bp)

    from app.routes.procurement import procurement_bp
    app.register_blueprint(procurement_bp)

    from app.routes.lab import lab_bp
    app.register_blueprint(lab_bp)

    from app.routes.reports import reports_bp
    app.register_blueprint(reports_bp)

    return app
