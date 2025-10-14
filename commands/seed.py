# seed.py
import click
from flask.cli import with_appcontext
from extensions import db
from models import Patient, Appointment
from datetime import date

@click.command("seed")
@with_appcontext
def seed():
    db.drop_all()
    db.create_all()

    p1 = Patient(name="Alice Dupont", age=29, diagnosis="Diabetes")
    p2 = Patient(name="Mohamed Ali", age=45, diagnosis="Hypertension")

    db.session.add_all([p1, p2])
    db.session.commit()

    a1 = Appointment(patient_id=p1.id, date=date.today(), note="Checkup")
    a2 = Appointment(patient_id=p2.id, date=date.today(), note="Follow-up")

    db.session.add_all([a1, a2])
    db.session.commit()

    print("✅ Database seeded with sample data")
