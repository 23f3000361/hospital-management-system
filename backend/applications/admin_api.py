from flask import request
from flask_restful import Resource
from .models import db, User, Appointment, Department, Treatment
from sqlalchemy.orm import joinedload
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
    get_jwt,
)
from datetime import datetime, date
from .api import cache

ALLOWED_REGISTRATION_ROLES = ["Doctor", "Patient"]
ALLOWED_ROLES = ["Admin", "Doctor", "Patient"]


from flask import request
from flask_restful import Resource
from .models import db, User, Appointment, Department
from sqlalchemy.orm import joinedload
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from datetime import datetime, date
from .api import cache

ALLOWED_REGISTRATION_ROLES = ["Doctor", "Patient"]
ALLOWED_ROLES = ["Admin", "Doctor", "Patient"]


class CreateDepartmentAPI(Resource):
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can create departments"}, 403

        data = request.json
        department_name = data.get("department_name")
        description = data.get("description", "")
        head_doctor_id = data.get("head_doctor_id")

        if not department_name or not 3 <= len(department_name.strip()) <= 100:
            return {"message": "Department name must be between 3 and 100 characters long"}, 400

        existing_dept = Department.query.filter_by(department_name=department_name.strip()).first()
        if existing_dept:
            return {"message": f"Department '{department_name}' already exists"}, 400

        head_doctor = None
        if head_doctor_id:
            head_doctor = User.query.filter_by(user_id=head_doctor_id, role="Doctor").first()
            if not head_doctor:
                return {"message": f"No doctor found with id {head_doctor_id}"}, 400

        new_department = Department(
            department_name=department_name.strip(),
            description=description.strip(),
            head_doctor_id=head_doctor.user_id if head_doctor else None,
        )
        db.session.add(new_department)
        db.session.commit()

        msg = f"Department '{new_department.department_name}' created successfully."
        if head_doctor:
            msg += f" Head doctor assigned: {head_doctor.name}"

        # Note: Creating a department doesn't directly affect the main doctor list cache, so no invalidation is strictly needed here.
        return {"message": msg}, 201


class AssignDoctorDepartmentAPI(Resource):
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can assign doctors to departments"}, 403

        data = request.json
        doctor_id = data.get("doctor_id")
        department_id = data.get("department_id")

        if not doctor_id or not department_id:
            return {"message": "Both doctor_id and department_id are required"}, 400

        doctor = User.query.filter_by(user_id=doctor_id, role="Doctor").first()
        if not doctor:
            return {"message": f"No doctor found with id {doctor_id}"}, 404

        department = Department.query.filter_by(department_id=department_id).first()
        if not department:
            return {"message": f"No department found with id {department_id}"}, 404

        doctor.department_id = department.department_id
        db.session.commit()

        # Invalidate the doctor list cache since a doctor's department has changed
        cache.delete('view//api/doctors')
        return {"message": f"Doctor {doctor.name} has been assigned to department {department.department_name}"}, 200


class AddDoctorAPI(Resource):
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can add new doctors"}, 403

        data = request.json
        # Check for required fields
        required = ["name", "email", "password", "qualification", "experience_years"]
        if not all(field in data and data[field] is not None for field in required):
            return {"message": "Name, email, password, qualification, and experience years are required"}, 400

        # Check for existing user
        if User.query.filter_by(email=data.get("email")).first():
            return {"message": f"User with email {data.get('email')} already exists"}, 409

        # --- MODIFIED: Robust Date of Birth Parsing ---
        dob_parsed = None
        dob_raw = data.get("date_of_birth")
        if dob_raw: # Only attempt to parse if the date is provided
            try:
                dob_parsed = datetime.strptime(str(dob_raw).strip(), '%Y-%m-%d').date()
            except (ValueError, TypeError):
                return {"message": "Invalid date format for date_of_birth. Please use YYYY-MM-DD."}, 400

        new_doctor = User(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            role="Doctor",
            phone=data.get("phone"),
            gender=data.get("gender"),
            date_of_birth=dob_parsed,
            address=data.get("address"),
            qualification=data.get("qualification"),
            experience_years=data.get("experience_years"),
        )
        db.session.add(new_doctor)
        db.session.commit()

        # Invalidate the doctor list cache
        cache.delete('view//api/doctors')
        return {"message": f"Doctor {new_doctor.name} added successfully.", "doctor_id": new_doctor.user_id}, 201


class EditDoctorAPI(Resource):
    @jwt_required()
    def put(self, doctor_id):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can edit doctor information"}, 403

        doctor = User.query.filter_by(user_id=doctor_id, role="Doctor").first()
        if not doctor:
            return {"message": "Doctor not found"}, 404

        data = request.json

        # --- MODIFIED: Handle date separately to prevent errors ---
        if 'date_of_birth' in data:
            dob_raw = data.get('date_of_birth')
            if dob_raw:
                try:
                    doctor.date_of_birth = datetime.strptime(str(dob_raw).strip(), '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    return {"message": "Invalid date format for date_of_birth. Please use YYYY-MM-DD."}, 400
            else:
                doctor.date_of_birth = None # Allow clearing the date

        # Update other allowed fields
        for key, value in data.items():
            if hasattr(doctor, key) and key not in ['date_of_birth', 'email', 'role']: # Don't update date here or critical fields
                setattr(doctor, key, value)

        # --- MODIFIED: Commit to DB before clearing cache ---
        db.session.commit()
        cache.delete('view//api/doctors')
        return {"message": f"Doctor {doctor.name}'s details updated successfully."}, 200


class DeleteDoctorAPI(Resource):
    @jwt_required()
    def delete(self, doctor_id):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can delete doctors"}, 403

        doctor = User.query.filter_by(user_id=doctor_id, role="Doctor").first()
        if not doctor:
            return {"message": "Doctor not found"}, 404

        db.session.delete(doctor)
        db.session.commit()

        cache.delete('view//api/doctors')
        return {"message": f"Doctor {doctor.name} and all associated data deleted successfully."}, 200


class BlacklistDoctorAPI(Resource):
    @jwt_required()
    def post(self, doctor_id):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can blacklist doctors"}, 403

        doctor = User.query.filter_by(user_id=doctor_id, role="Doctor").first()
        if not doctor:
            return {"message": "Doctor not found"}, 404

        if doctor.status == "Inactive":
            return {"message": f"Doctor {doctor.name} is already blacklisted"}, 400

        doctor.status = "Inactive"
        db.session.commit()

        cache.delete('view//api/doctors')
        return {"message": f"Doctor {doctor.name} has been blacklisted successfully."}, 200


class EditPatientAPI(Resource):
    @jwt_required()
    def put(self, patient_id):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can edit patient information"}, 403

        patient = User.query.filter_by(user_id=patient_id, role="Patient").first()
        if not patient:
            return {"message": "Patient not found"}, 404

        data = request.json

        # --- MODIFIED: Handle date separately to prevent errors ---
        if 'date_of_birth' in data:
            dob_raw = data.get('date_of_birth')
            if dob_raw:
                try:
                    patient.date_of_birth = datetime.strptime(str(dob_raw).strip(), '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    return {"message": "Invalid date format for date_of_birth. Please use YYYY-MM-DD."}, 400
            else:
                patient.date_of_birth = None # Allow clearing the date

        for key, value in data.items():
            if hasattr(patient, key) and key not in ['date_of_birth', 'email', 'role']:
                setattr(patient, key, value)

        db.session.commit()
        cache.delete('view//api/admin/patients')
        return {"message": f"Patient {patient.name}'s details updated successfully."}, 200


class DeletePatientAPI(Resource):
    @jwt_required()
    def delete(self, patient_id):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can delete patients"}, 403

        patient = User.query.filter_by(user_id=patient_id, role="Patient").first()
        if not patient:
            return {"message": "Patient not found"}, 404

        db.session.delete(patient)
        db.session.commit()

        # --- ADDED: Missing cache invalidation ---
        cache.delete('view//api/admin/patients')
        return {"message": f"Patient {patient.name} and all associated data deleted successfully."}, 200


class BlacklistPatientAPI(Resource):
    @jwt_required()
    def post(self, patient_id):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can blacklist patients"}, 403

        patient = User.query.filter_by(user_id=patient_id, role="Patient").first()
        if not patient:
            return {"message": "Patient not found"}, 404

        if patient.status == "Inactive":
            return {"message": f"Patient {patient.name} is already blacklisted"}, 400

        patient.status = "Inactive"
        db.session.commit()

        # --- ADDED: Missing cache invalidation ---
        cache.delete('view//api/admin/patients')
        return {"message": f"Patient {patient.name} has been blacklisted successfully."}, 200


class AdminViewPatientHistoryAPI(Resource):
    @jwt_required()
    def get(self, patient_id):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can view patient history"}, 403

        patient = User.query.filter_by(user_id=patient_id, role="Patient").first()
        if not patient:
            return {"message": "Patient not found"}, 404

        upcoming_only = request.args.get("upcoming_only", "false").lower() == "true"
        query = Appointment.query.filter_by(patient_id=patient_id).options(
            joinedload(Appointment.doctor), joinedload(Appointment.treatment)
        )
        if upcoming_only:
            query = query.filter(Appointment.date >= date.today())

        appointments = query.all()

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


class PatientListAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can view patient list"}, 403

        patients = User.query.filter_by(role="Patient").all()
        result = [
            {
                "user_id": p.user_id,
                "name": p.name,
                "email": p.email,
                "phone": p.phone,
                "status": p.status,
                "date_of_birth": p.date_of_birth,
            }
            for p in patients
        ]
        return {"patients": result}, 200


class UpcomingAppointmentsAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can view upcoming appointments"}, 403

        appointments = (
            Appointment.query.filter(Appointment.date >= date.today())
            .options(joinedload(Appointment.patient), joinedload(Appointment.doctor))
            .order_by(Appointment.date, Appointment.time)
            .all()
        )

        result = [
            {
                "appointment_id": appt.appointment_id,
                "patient_name": appt.patient.name,
                "doctor_name": appt.doctor.name,
                "department": (
                    appt.doctor.department.department_name
                    if appt.doctor.department
                    else "N/A"
                ),
                "date": str(appt.date),
                "time": appt.time,
                "status": appt.status,
            }
            for appt in appointments
        ]
        return {"upcoming_appointments": result}, 200


class AdminFeeReportAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"message": "Only admins can view financial reports"}, 403
        appointments = db.session.query(
            Appointment.payment_status, Appointment.fee_amount
        ).all()
        total_collected = 0.0
        total_outstanding = 0.0
        fees_by_status = {"Paid": 0.0, "Unpaid": 0.0, "Pending": 0.0}
        for status, amount in appointments:
            if amount:
                if status == "Paid":
                    total_collected += amount
                    fees_by_status["Paid"] += amount
                elif status == "Unpaid":
                    total_outstanding += amount
                    fees_by_status["Unpaid"] += amount
                elif status == "Pending":
                    fees_by_status["Pending"] += amount
        return {
            "message": "Fee report generated successfully",
            "summary": {
                "total_collected_fees": total_collected,
                "total_outstanding_fees": total_outstanding,
                "fees_by_status": fees_by_status,
            },
        }, 200
