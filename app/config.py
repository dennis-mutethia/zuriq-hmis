import os


class Config:
    # Supabase gives you a connection string under
    # Project Settings -> Database -> Connection string -> URI.
    # Use the "Transaction" pooler string for most app workloads.
    # Put it in a .env file (see .env.example) — never commit real credentials.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
