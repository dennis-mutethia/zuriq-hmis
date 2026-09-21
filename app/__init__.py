from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.nav import nav_link
    app.jinja_env.globals["nav_link"] = nav_link

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.patients import patients_bp
    app.register_blueprint(patients_bp)

    from app.routes.visits import visits_bp
    app.register_blueprint(visits_bp)

    from app.routes.billing import billing_bp
    app.register_blueprint(billing_bp)

    from app.routes.admissions import admissions_bp
    app.register_blueprint(admissions_bp)

    from app.routes.pharmacy import pharmacy_bp
    app.register_blueprint(pharmacy_bp)

    from app.routes.lab import lab_bp
    app.register_blueprint(lab_bp)

    return app
