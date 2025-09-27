from flask import request, send_file
from flask_restful import Resource
from .models import db, User, Appointment, Department
from sqlalchemy.orm import joinedload
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from datetime import datetime, date
import io
import csv

ALLOWED_REGISTRATION_ROLES = ["Doctor", "Patient"]
ALLOWED_ROLES = ["Admin", "Doctor", "Patient"]


class PatientProfileAPI(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Patient":
            return {"message": "Only patients can view their profile"}, 403

        patient_id = get_jwt_identity()
        patient = User.query.filter_by(user_id=patient_id, role="Patient").first()

        if not patient:
            return {"message": "Patient not found"}, 404

        return {
            "user_id": patient.user_id,
            "name": patient.name,
            "email": patient.email,
            "phone": patient.phone,
            "gender": patient.gender,
            "date_of_birth": patient.date_of_birth,
            "address": patient.address,
            "emergency_contact": patient.emergency_contact,
            "blood_group": patient.blood_group,
            "status": patient.status,
            "role": patient.role,
        }, 200

    @jwt_required()
    def put(self):
        claims = get_jwt()
        if claims.get("role") != "Patient":
            return {"message": "Only patients can edit their profile"}, 403

        patient_id = get_jwt_identity()
        patient = User.query.filter_by(user_id=patient_id, role="Patient").first()

        if not patient:
            return {"message": "Patient not found"}, 404

        data = request.json
        for key, value in data.items():
            if hasattr(patient, key) and key not in [
                "user_id",
                "email",
                "role",
                "password",
            ]:
                setattr(patient, key, value)

        db.session.commit()
        return {"message": "Profile updated successfully"}, 200


class PatientAppointmentsAPI(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Patient":
            return {"message": "Only patients can view their appointments"}, 403

        patient_id = get_jwt_identity()

        # Get query parameters for filtering (e.g., upcoming_only)
        upcoming_only = request.args.get("upcoming_only", "false").lower() == "true"

        query = Appointment.query.filter_by(patient_id=patient_id).options(
            joinedload(Appointment.doctor).joinedload(User.department)
        )

        if upcoming_only:
            query = query.filter(Appointment.date >= date.today())

        appointments = query.order_by(Appointment.date, Appointment.time).all()

        result = []
        for appt in appointments:
            doctor_name = appt.doctor.name if appt.doctor else "N/A"
            department_name = (
                appt.doctor.department.department_name
                if appt.doctor and appt.doctor.department
                else "N/A"
            )

            result.append(
                {
                    "appointment_id": appt.appointment_id,
                    "doctor_name": doctor_name,
                    "department": department_name,
                    "date": str(appt.date),
                    "time": appt.time,
                    "status": appt.status,
                }
            )
        return {"appointments": result}, 200

    @jwt_required()
    def delete(self, appointment_id):
        claims = get_jwt()
        if claims.get("role") != "Patient":
            return {"message": "Only patients can cancel appointments"}, 403

        patient_id = get_jwt_identity()
        appointment = Appointment.query.filter_by(
            appointment_id=appointment_id, patient_id=patient_id
        ).first()

        if not appointment:
            return {"message": "Appointment not found or you are not the patient"}, 404

        if appointment.date < date.today():
            return {"message": "Cannot cancel past appointments"}, 400

        appointment.status = "Cancelled"
        db.session.commit()
        return {"message": f"Appointment {appointment_id} has been cancelled."}, 200


class DepartmentListAPI(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") not in ["Admin", "Patient"]:  # Both can view departments
            return {"message": "Access denied"}, 403

        departments = Department.query.all()
        result = [
            {
                "department_id": d.department_id,
                "department_name": d.department_name,
                "description": d.description,
                "head_doctor": d.head_doctor.name if d.head_doctor else "N/A",
            }
            for d in departments
        ]
        return {"departments": result}, 200


class DepartmentDoctorsAPI(Resource):
    @jwt_required()
    def get(self, department_id):
        claims = get_jwt()
        if claims.get("role") not in ["Admin", "Patient"]:
            return {"message": "Access denied"}, 403

        department = Department.query.get(department_id)
        if not department:
            return {"message": "Department not found"}, 404

        doctors = User.query.filter_by(
            department_id=department_id, role="Doctor", status="Active"
        ).all()

        result = [
            {
                "user_id": d.user_id,
                "name": d.name,
                "email": d.email,
                "phone": d.phone,
                "qualification": d.qualification,
                "experience_years": d.experience_years,
            }
            for d in doctors
        ]
        return {"department_name": department.department_name, "doctors": result}, 200


class DoctorProfilePatientViewAPI(Resource):
    @jwt_required()
    def get(self, doctor_id):
        claims = get_jwt()
        if claims.get("role") not in ["Admin", "Patient"]:
            return {"message": "Access denied"}, 403

        doctor = (
            User.query.filter_by(user_id=doctor_id, role="Doctor", status="Active")
            .options(joinedload(User.department))
            .first()
        )

        if not doctor:
            return {"message": "Doctor not found or inactive"}, 404

        return {
            "user_id": doctor.user_id,
            "name": doctor.name,
            "email": doctor.email,
            "phone": doctor.phone,
            "gender": doctor.gender,
            "qualification": doctor.qualification,
            "experience_years": doctor.experience_years,
            "department": (
                doctor.department.department_name if doctor.department else "N/A"
            ),
        }, 200


class PatientBookAppointmentAPI(
    Resource
):  # Already existed, but including for completeness
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims.get("role") != "Patient":
            return {"message": "Only patients can book appointments"}, 403

        data = request.json
        doctor_id = data.get("doctor_id")
        date_str = data.get("date")
        time = data.get("time")

        if not doctor_id or not date_str or not time:
            return {"message": "doctor_id, date and time required"}, 400

        try:
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return {"message": "Date format should be YYYY-MM-DD"}, 400

        if appointment_date < date.today():
            return {"message": "Cannot book appointments in the past"}, 400

        doctor = User.query.filter_by(
            user_id=doctor_id, role="Doctor", status="Active"
        ).first()
        if not doctor:
            return {"message": "Doctor not found or inactive"}, 404

        # Check for existing appointment at the same time for this doctor
        existing_appt = Appointment.query.filter_by(
            doctor_id=doctor_id, date=appointment_date, time=time, status="Booked"
        ).first()
        if existing_appt:
            return {"message": "Doctor is already booked at this time"}, 409  # Conflict

        patient_id = get_jwt_identity()
        new_appt = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=appointment_date,
            time=time,
            status="Booked",
        )
        db.session.add(new_appt)
        db.session.commit()

        return {
            "message": f"Appointment booked with Doctor {doctor.name} on {date_str} at {time}"
        }, 201


class PatientHistoryExportCSVAPI(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Patient":
            return {"message": "Only patients can export their history"}, 403

        patient_id = get_jwt_identity()
        patient = User.query.filter_by(user_id=patient_id, role="Patient").first()
        if not patient:
            return {"message": "Patient not found"}, 404

        appointments = (
            Appointment.query.filter_by(patient_id=patient_id)
            .options(joinedload(Appointment.doctor), joinedload(Appointment.treatment))
            .order_by(Appointment.date.desc(), Appointment.time.desc())
            .all()
        )

        output = io.StringIO()
        writer = csv.writer(output)

        # CSV Header
        writer.writerow(
            [
                "Appointment ID",
                "Doctor Name",
                "Date",
                "Time",
                "Status",
                "Diagnosis",
                "Prescription",
                "Notes",
            ]
        )

        for appt in appointments:
            diagnosis = appt.treatment.diagnosis if appt.treatment else ""
            prescription = appt.treatment.prescription if appt.treatment else ""
            notes = appt.treatment.notes if appt.treatment else ""

            writer.writerow(
                [
                    appt.appointment_id,
                    appt.doctor.name if appt.doctor else "N/A",
                    str(appt.date),
                    appt.time,
                    appt.status,
                    diagnosis,
                    prescription,
                    notes,
                ]
            )

        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode("utf-8")),
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"patient_{patient_id}_history.csv",
        )


class DoctorListAPI(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") not in ["Admin", "Patient"]:
            return {"message": "Access denied"}, 403

        doctors = User.query.filter_by(role="Doctor").all()
        result = [
            {
                "user_id": d.user_id,
                "name": d.name,
                "email": d.email,
                "phone": d.phone,
                "department": d.department.department_name if d.department else "N/A",
                "status": d.status,
            }
            for d in doctors
        ]
        return {"doctors": result}, 200
