from flask import request
from flask_restful import Resource
from .models import db, User, Appointment, Treatment
from sqlalchemy.orm import joinedload
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from .api import cache
from datetime import datetime, date

ALLOWED_REGISTRATION_ROLES = ["Doctor", "Patient"]
ALLOWED_ROLES = ["Admin", "Doctor", "Patient"]


class DoctorAppointmentsAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can view appointments"}, 403

        doctor_id = get_jwt_identity()
        appointments = (
            Appointment.query.filter_by(doctor_id=doctor_id)
            .order_by(Appointment.date.desc())
            .all()
        )
        result = [
            {
                "appointment_id": a.appointment_id,
                "patient_id": a.patient_id,
                "date": str(a.date),
                "time": a.time,
                "status": a.status,
            }
            for a in appointments
        ]
        return {"appointments": result}, 200

    @jwt_required()
    def put(self, appointment_id):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can update appointments"}, 403

        appointment = Appointment.query.filter_by(
            appointment_id=appointment_id, doctor_id=get_jwt_identity()
        ).first()
        if not appointment:
            return {
                "message": "Appointment not found or you are not the assigned doctor"
            }, 404

        appointment.status = "Cancelled"
        db.session.commit()
        return {"message": f"Appointment {appointment_id} has been cancelled."}, 200


class CompleteAppointmentAPI(Resource):
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can complete appointments"}, 403

        data = request.json
        appointment_id = data.get("appointment_id")
        diagnosis = data.get("diagnosis")
        prescription = data.get("prescription")
        notes = data.get("notes")

        appt = Appointment.query.filter_by(
            appointment_id=appointment_id, doctor_id=get_jwt_identity()
        ).first()
        if not appt:
            return {"message": "Appointment not found"}, 404

        appt.status = "Completed"
        treatment = Treatment(
            appointment_id=appointment_id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes,
        )
        db.session.add(treatment)
        db.session.commit()

        return {
            "message": f"Appointment {appointment_id} marked completed with treatment"
        }, 200


class DoctorViewPatientHistoryAPI(Resource):
    @jwt_required()
    def get(self, patient_id):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can view patient history"}, 403

        doctor_id = get_jwt_identity()

        patient = User.query.filter_by(user_id=patient_id, role="Patient").first()
        if not patient:
            return {"message": "Patient not found"}, 404

        is_assigned = Appointment.query.filter_by(
            patient_id=patient_id, doctor_id=doctor_id
        ).first()
        if not is_assigned:
            return {"message": "Access denied. This is not your patient."}, 403

        appointments = (
            Appointment.query.filter_by(patient_id=patient_id)
            .options(joinedload(Appointment.doctor), joinedload(Appointment.treatment))
            .all()
        )

        patient_history = {"patient_name": patient.name, "appointments": []}

        for appt in appointments:
            appt_data = {
                "appointment_id": appt.appointment_id,
                "doctor_name": appt.doctor.name if appt.doctor else "N/A",
                "date": str(appt.date),
                "time": appt.time,
                "status": appt.status,
                "treatment_details": None,
            }
            if appt.treatment:
                appt_data["treatment_details"] = {
                    "diagnosis": appt.treatment.diagnosis,
                    "prescription": appt.treatment.prescription,
                    "notes": appt.treatment.notes,
                }

            patient_history["appointments"].append(appt_data)

        return patient_history, 200


class AssignedPatientsAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can view their assigned patients"}, 403

        doctor_id = get_jwt_identity()

        patients = (
            db.session.query(User)
            .join(Appointment, User.user_id == Appointment.patient_id)
            .filter(Appointment.doctor_id == doctor_id)
            .distinct()
            .all()
        )

        result = [
            {
                "patient_id": p.user_id,
                "name": p.name,
                "email": p.email,
                "phone": p.phone,
            }
            for p in patients
        ]
        return {"assigned_patients": result}, 200


class DoctorAvailabilityAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can view their availability"}, 403

        return {
            "message": "Doctor availability feature not yet fully implemented. Please check back later."
        }, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can update their availability"}, 403

        data = request.json
        availability_data = data.get("availability")

        if not availability_data:
            return {"message": "Availability data is required"}, 400

        return {"message": "Doctor availability updated successfully."}, 200
