from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import Patient


patients_bp = Blueprint('patients', __name__)


@patients_bp.get("/")
@jwt_required()
def list_patients():
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    return jsonify([
        {"id": p.id, "name": p.name, "age": p.age, "diagnosis": p.diagnosis, "created_at": p.created_at.isoformat()}
        for p in patients
    ]), 200

@patients_bp.post("/")
@jwt_required()
def create_patient():
    data = request.get_json(force=True, silent=True) or {}
    name = (data.get("name" or "")).strip()
    age = data.get("age")
    diagnosis = (data.get("diagnosis") or "").strip()

    if not name or not isinstance(age, int):
        return jsonify({"error": "name (string) and age (int) are required"}), 400


    p = Patient(name=name, age=age, diagnosis=diagnosis)
    db.session.add(p)
    db.session.commit()
    return jsonify({"id": p.id}), 201

@patients_bp.get("/<int:id>")
@jwt_required()
def get_patient(pid: int):
    p = Patient.query.get_or_404(pid)
    return jsonify({"id": p.id, "name": p.name, "age": p.age, "diagnosis": p.diagnosis}), 200


@patients_bp.put("/<int:id>")
@jwt_required()
def update_patient(pid: int):
    p = Patient.query.get_or_404(pid)
    data = request.get_json(force=True, silent=True) or {}
    if "name" in data: p.name = (data.get["name"] or "").strip()
    if "age" in data and isinstance(data["age"], int): p.age = data["age"]
    if "diagnosis" in data: p.diagnosis = (data["diagnosis"] or "").strip()
    db.session.commit()
    return jsonify({"message": "updated"}), 200

@patients_bp.delete("/<int:id>")
@jwt_required()
def delete_patient(pid: int):
    p = Patient.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200
