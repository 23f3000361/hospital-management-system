from flask import Flask, request
from flask_restful import Api
from applications.models import db, User
from applications.api import WelcomeAPI
from applications.auth_api import LoginAPI, SignUpAPI
from applications.admin_api import (
    CreateDepartmentAPI,
    AssignDoctorDepartmentAPI,
    AddDoctorAPI,
    EditDoctorAPI,
    DeleteDoctorAPI,
    BlacklistDoctorAPI,
    EditPatientAPI,
    DeletePatientAPI,
    BlacklistPatientAPI,
    AdminViewPatientHistoryAPI,
    PatientListAPI,
    UpcomingAppointmentsAPI,
)
from applications.doctor_api import (
    DoctorAppointmentsAPI,
    CompleteAppointmentAPI,
    DoctorViewPatientHistoryAPI,
    AssignedPatientsAPI,
    DoctorAvailabilityAPI,
)
from applications.patient_api import (
    DoctorListAPI,
    PatientProfileAPI,
    PatientAppointmentsAPI,
    DepartmentListAPI,
    DoctorProfilePatientViewAPI,
    PatientHistoryExportCSVAPI,
    DepartmentDoctorsAPI,
    PatientBookAppointmentAPI,
)
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    base_dir, "database.sqlite3"
)
app.config["SECRET_KEY"] = "very-secret"
app.config["JWT_SECRET_KEY"] = "very-very-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

db.init_app(app)
api = Api(app)
app.app_context().push()
jwt = JWTManager(app)


def add_admin():
    admin = User.query.filter(
        (User.name == "Admin") | (User.email == "admin@gmail.com")
    ).first()
    if not admin:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password="1234",
            status="Active",
            role="Admin",
        )
        db.session.add(admin)
        db.session.commit()
        return "Admin added"
    else:
        return "Admin already exists:", admin.name, admin.email


api.add_resource(WelcomeAPI, "/api/welcome")
api.add_resource(LoginAPI, "/api/login")
api.add_resource(SignUpAPI, "/api/signup")
api.add_resource(CreateDepartmentAPI, "/api/add_dept")
api.add_resource(AssignDoctorDepartmentAPI, "/api/assign_doctor")
api.add_resource(AddDoctorAPI, "/api/admin/add_doctor")
api.add_resource(EditDoctorAPI, "/api/admin/doctor/edit/<int:doctor_id>")
api.add_resource(DeleteDoctorAPI, "/api/admin/doctor/delete/<int:doctor_id>")
api.add_resource(BlacklistDoctorAPI, "/api/admin/doctor/blacklist/<int:doctor_id>")
api.add_resource(EditPatientAPI, "/api/admin/patient/edit/<int:patient_id>")
api.add_resource(DeletePatientAPI, "/api/admin/patient/delete/<int:patient_id>")
api.add_resource(BlacklistPatientAPI, "/api/admin/patient/blacklist/<int:patient_id>")
api.add_resource(
    AdminViewPatientHistoryAPI, "/api/admin/patient/history/<int:patient_id>"
)
api.add_resource(DoctorListAPI, "/api/doctors")
api.add_resource(PatientListAPI, "/api/admin/patients")
api.add_resource(UpcomingAppointmentsAPI, "/api/admin/upcoming_appointments")
api.add_resource(
    DoctorAppointmentsAPI,
    "/api/doctor/appointments",
    "/api/doctor/appointments/<int:appointment_id>",
)
api.add_resource(CompleteAppointmentAPI, "/api/doctor/complete_appointment")
api.add_resource(
    DoctorViewPatientHistoryAPI, "/api/doctor/patient_history/<int:patient_id>"
)
api.add_resource(AssignedPatientsAPI, "/api/doctor/assigned_patients")
api.add_resource(DoctorAvailabilityAPI, "/api/doctor/availability")
api.add_resource(PatientProfileAPI, "/api/patient/profile")
api.add_resource(
    PatientAppointmentsAPI,
    "/api/patient/appointments",
    "/api/patient/appointments/<int:appointment_id>",
)
api.add_resource(DepartmentListAPI, "/api/departments")
api.add_resource(DepartmentDoctorsAPI, "/api/departments/<int:department_id>/doctors")
api.add_resource(DoctorProfilePatientViewAPI, "/api/doctors/<int:doctor_id>")
api.add_resource(PatientBookAppointmentAPI, "/api/patient/book_appointment")
api.add_resource(PatientHistoryExportCSVAPI, "/api/patient/history/export_csv")


@app.route("/")
def home():
    return "Hello World!"


if __name__ == "__main__":
    db.create_all()
    add_admin()
    app.run(debug=True)
