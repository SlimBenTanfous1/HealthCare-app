from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="doctor")

    def set_password(self, plain: str):
        self.password_hash = generate_password_hash(plain)

    def verify_password(self, plain: str) -> bool:
        return check_password_hash(self.password_hash, plain)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    age = db.Column(db.Integer, nullable=False)
    diagnosis = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False, index=True)
    date = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(255))
    patient = db.relationship("Patient", backref="appointments", lazy=True)
