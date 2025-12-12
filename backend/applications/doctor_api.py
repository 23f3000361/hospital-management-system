from flask import request
from flask_restful import Resource
from .models import db, User, Appointment, Treatment, DoctorAvailability
from sqlalchemy.orm import joinedload
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from .api import cache
from datetime import datetime, date, timedelta

class DoctorProfileAPI(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Access denied"}, 403

        doctor_id = get_jwt_identity()
        doctor = User.query.filter_by(user_id=doctor_id).first()

        if not doctor:
            return {"message": "Doctor not found"}, 404

        return {
            "name": doctor.name,
            "email": doctor.email,
            "phone": doctor.phone
        }, 200

class DoctorAppointmentsAPI(Resource):
    @jwt_required()
    # REMOVED CACHE to fix the "Data comes back on refresh" issue
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can view appointments"}, 403

        doctor_id = get_jwt_identity()

        # Added joinedload(Appointment.patient) to ensure Patient Name is visible
        appointments = (
            Appointment.query.filter_by(doctor_id=doctor_id)
            .filter(Appointment.status == "Booked")
            .options(joinedload(Appointment.patient))
            .order_by(Appointment.date.asc(), Appointment.time.asc())
            .all()
        )

        result = []
        for a in appointments:
            # Safety check if patient relationship exists
            p_name = a.patient.name if a.patient else "Unknown Patient"

            result.append({
                "appointment_id": a.appointment_id,
                "patient_id": a.patient_id,
                "patient_name": p_name, # Fixed: ensured data is loaded
                "date": str(a.date),
                "time": a.time,
                "status": a.status,
            })

        return {"appointments": result}, 200

    @jwt_required()
    def put(self, appointment_id):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can update appointments"}, 403

        doctor_id = get_jwt_identity()
        appointment = Appointment.query.filter_by(
            appointment_id=appointment_id, doctor_id=doctor_id
        ).first()

        if not appointment:
            return {"message": "Appointment not found"}, 404

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

        doctor_id = get_jwt_identity()
        appt = Appointment.query.filter_by(
            appointment_id=appointment_id, doctor_id=doctor_id
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
            "message": "Appointment marked as completed successfully."
        }, 200

class DoctorViewPatientHistoryAPI(Resource):
    @jwt_required()
    def get(self, patient_id):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can view patient history"}, 403

        patient = User.query.filter_by(user_id=patient_id, role="Patient").first()
        if not patient:
            return {"message": "Patient not found"}, 404

        appointments = (
            Appointment.query.filter_by(patient_id=patient_id)
            .options(joinedload(Appointment.doctor), joinedload(Appointment.treatment))
            .order_by(Appointment.date.desc())
            .all()
        )

        history = []
        for appt in appointments:
            appt_data = {
                "date": str(appt.date),
                "doctor_name": appt.doctor.name if appt.doctor else "N/A",
                "diagnosis": appt.treatment.diagnosis if appt.treatment else "N/A",
                "prescription": appt.treatment.prescription if appt.treatment else "N/A",
                "notes": appt.treatment.notes if appt.treatment else "N/A",
            }
            history.append(appt_data)

        return {"patient_name": patient.name, "history": history}, 200

class AssignedPatientsAPI(Resource):
    @jwt_required()
    # REMOVED CACHE to fix refresh issues
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Only doctors can view assigned patients"}, 403

        doctor_id = get_jwt_identity()

        # FIX: Only show patients who have 'Booked' (Active) appointments
        patients = (
            db.session.query(User)
            .join(Appointment, User.user_id == Appointment.patient_id)
            .filter(Appointment.doctor_id == doctor_id)
            .filter(Appointment.status == "Booked") # <--- ADDED THIS FILTER
            .distinct()
            .all()
        )

        result = [
            {
                "patient_id": p.user_id,
                "name": p.name,
                "email": p.email
            }
            for p in patients
        ]
        return {"assigned_patients": result}, 200

class DoctorAvailabilityAPI(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Access denied"}, 403

        doctor_id = get_jwt_identity()
        today = date.today()
        availability_list = []

        for i in range(7):
            current_date = today + timedelta(days=i)

            record = DoctorAvailability.query.filter_by(
                doctor_id=doctor_id,
                date=current_date
            ).first()

            if record:
                availability_list.append({
                    "date": current_date.strftime("%d/%m/%Y"),
                    "morning": record.available_morning,
                    "evening": record.available_evening
                })
            else:
                availability_list.append({
                    "date": current_date.strftime("%d/%m/%Y"),
                    "morning": True,
                    "evening": True
                })

        return {"availability": availability_list}, 200

    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims.get("role") != "Doctor":
            return {"message": "Access denied"}, 403

        doctor_id = get_jwt_identity()
        data = request.json
        availability_data = data.get("availability")

        if not availability_data:
            return {"message": "No data provided"}, 400

        try:
            for day_data in availability_data:
                date_obj = datetime.strptime(day_data['date'], "%d/%m/%Y").date()

                record = DoctorAvailability.query.filter_by(
                    doctor_id=doctor_id,
                    date=date_obj
                ).first()

                if record:
                    record.available_morning = day_data['morning']
                    record.available_evening = day_data['evening']
                else:
                    new_record = DoctorAvailability(
                        doctor_id=doctor_id,
                        date=date_obj,
                        available_morning=day_data['morning'],
                        available_evening=day_data['evening']
                    )
                    db.session.add(new_record)

            db.session.commit()
            return {"message": "Availability updated successfully."}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error saving availability: {str(e)}"}, 500