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

    # ⚡ Priorité à la variable d’env du CI/CD
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///instance/healthcare.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")

    db.init_app(app)

    # enregistre les blueprints...
    return app

    # --- Simple home page ---
    @app.get("/")
    def home():
        return render_template("index.html")

    return app

app = create_app()

if __name__ == "__main__":
    # Local dev: bind localhost; Docker will use gunicorn (see Dockerfile)
    app.run(host="127.0.0.1", port=5000)
