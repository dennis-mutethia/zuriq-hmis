from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.patients import patients_bp
    app.register_blueprint(patients_bp)

    from app.routes.visits import visits_bp
    app.register_blueprint(visits_bp)

    return app
