from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import Appointment, Patient

appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.get("/")
@jwt_required()
def list_appointments():
    items = Appointment.query.order_by(Appointment.id.desc()).all()
    return jsonify([
        {
            "id": a.id,
            "patient_id": a.patient_id,
            "date": a.date,
            "note": a.note
        }
        for a in items
    ]), 200


@appointments_bp.post("/")
@jwt_required()
def create_appointment():
    data = request.get_json(force=True, silent=True) or {}
    patient_id = data.get("patient_id")
    date = (data.get("date") or "").strip()
    note = (data.get("note") or "").strip()

    # Validation basique
    if not isinstance(patient_id, int) or not date:
        return jsonify({"error": "patient_id (int) and date (string) are required"}), 400

    # Vérification que le patient existe
    patient = db.session.get(Patient, patient_id)
    if not patient:
        return jsonify({"error": "patient not found"}), 404

    a = Appointment(patient_id=patient_id, date=date, note=note)
    db.session.add(a)
    db.session.commit()
    return jsonify({"id": a.id}), 201


@appointments_bp.delete("/<int:aid>")
@jwt_required()
def delete_appointment(aid: int):
    a = db.session.get(Appointment, aid)
    if not a:
        return jsonify({"error": "appointment not found"}), 404

    db.session.delete(a)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200
