import os
from flask import Flask, render_template
from dotenv import load_dotenv
from extensions import db, jwt, migrate
from routes.auth import auth_bp
from routes.patients import patients_bp
from routes.appointments import appointments_bp

load_dotenv()  # loads .env if present

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///instance/healthcare.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")

    db.init_app(app)
    jwt.init_app(app)

    # --- Register blueprints ---
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(patients_bp, url_prefix="/patients")
    app.register_blueprint(appointments_bp, url_prefix="/appointments")

    # --- Simple home page ---
    @app.get("/")
    def home():
        return render_template("index.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
