from flask import Flask
from flask_restful import Api
from applications.models import db, User
from applications.api import WelcomeAPI, cache
from applications.auth_api import LoginAPI, SignUpAPI
from applications.admin_api import (
    CreateDepartmentAPI, AssignDoctorDepartmentAPI, AddDoctorAPI, EditDoctorAPI,
    DeleteDoctorAPI, BlacklistDoctorAPI, EditPatientAPI, DeletePatientAPI,
    BlacklistPatientAPI, AdminViewPatientHistoryAPI, PatientListAPI,
    UpcomingAppointmentsAPI, AdminFeeReportAPI, AdminDoctorListAPI,
    DepartmentListAPI, EditDepartmentAPI
)
from applications.doctor_api import (
    DoctorAppointmentsAPI, CompleteAppointmentAPI, DoctorViewPatientHistoryAPI,
    AssignedPatientsAPI, DoctorAvailabilityAPI, DoctorProfileAPI
)
from applications.patient_api import (
    DoctorListAPI, PatientProfileAPI, PatientAppointmentsAPI,
    DoctorProfilePatientViewAPI, PatientHistoryExportCSVAPI, DepartmentDoctorsAPI,
    PatientBookAppointmentAPI, PaymentAPI, ExportPatientHistoryAPI,
    PatientViewDoctorAvailabilityAPI
)
from applications.worker import celery_init_app
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from celery.schedules import crontab

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# --- Database Config ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "database.sqlite3")
app.config["SECRET_KEY"] = "very-secret"

# --- JWT Config ---
app.config["JWT_SECRET_KEY"] = "very-very-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
app.config['JWT_DECODE_LEEWAY'] = 10

# --- Redis Cache Config ---
app.config["CACHE_TYPE"] = "simple"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_REDIS_DB"] = 0
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

# --- Celery Configuration ---
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"
app.config["CELERY_TIMEZONE"] = "Asia/Kolkata"

# Define Scheduled Jobs (Celery Beat)
app.config["CELERY_BEAT_SCHEDULE"] = {
    'daily-reminder-morning': {
        'task': 'applications.task.send_daily_reminders',
        # Runs daily at 9:00 AM
        'schedule': crontab(hour=9, minute=0),
    },
    'monthly-report-1st': {
        'task': 'applications.task.generate_monthly_report',
        # Runs on the 1st of every month at 8:00 AM
        'schedule': crontab(day_of_month=1, hour=8, minute=0),
    },
}

# --- Initialization ---
db.init_app(app)
cache.init_app(app)
api = Api(app)
jwt = JWTManager(app)

# Initialize Celery
celery = celery_init_app(app)

# Import Tasks AFTER celery init so they register correctly
import applications.task

app.app_context().push()

@app.route("/test_cache")
@cache.cached(timeout=10)
def test_cache():
    return "Cache test is working fine."

def add_admin():
    admin = User.query.filter((User.name == "Admin") | (User.email == "admin@gmail.com")).first()
    if not admin:
        admin = User(name="Admin", email="admin@gmail.com", password="1234", status="Active", role="Admin")
        db.session.add(admin)
        db.session.commit()
        return "Admin added"
    else:
        return "Admin already exists"

# --- API Resources ---
api.add_resource(WelcomeAPI, "/api/welcome")
api.add_resource(LoginAPI, "/api/login")
api.add_resource(SignUpAPI, "/api/signup")

# Admin
api.add_resource(CreateDepartmentAPI, "/api/add_dept")
api.add_resource(AssignDoctorDepartmentAPI, "/api/assign_doctor")
api.add_resource(AdminDoctorListAPI, "/api/admin/doctors")
api.add_resource(AddDoctorAPI, "/api/admin/add_doctor")
api.add_resource(EditDoctorAPI, "/api/admin/doctor/edit/<int:doctor_id>")
api.add_resource(DeleteDoctorAPI, "/api/admin/doctor/delete/<int:doctor_id>")
api.add_resource(BlacklistDoctorAPI, "/api/admin/doctor/blacklist/<int:doctor_id>")
api.add_resource(EditPatientAPI, "/api/admin/patient/edit/<int:patient_id>")
api.add_resource(DeletePatientAPI, "/api/admin/patient/delete/<int:patient_id>")
api.add_resource(BlacklistPatientAPI, "/api/admin/patient/blacklist/<int:patient_id>")
api.add_resource(AdminViewPatientHistoryAPI, "/api/admin/patient/history/<int:patient_id>")
api.add_resource(EditDepartmentAPI, "/api/admin/department/edit/<int:department_id>")
api.add_resource(DoctorListAPI, "/api/doctors")
api.add_resource(PatientListAPI, "/api/admin/patients")
api.add_resource(UpcomingAppointmentsAPI, "/api/admin/upcoming_appointments")
api.add_resource(AdminFeeReportAPI, "/api/admin/reports/fees")
api.add_resource(DepartmentListAPI, "/api/departments")

# Doctor
api.add_resource(DoctorAppointmentsAPI, "/api/doctor/appointments", "/api/doctor/appointments/<int:appointment_id>")
api.add_resource(DoctorProfileAPI, "/api/doctor/profile")
api.add_resource(CompleteAppointmentAPI, "/api/doctor/complete_appointment")
api.add_resource(DoctorViewPatientHistoryAPI, "/api/doctor/patient_history/<int:patient_id>")
api.add_resource(AssignedPatientsAPI, "/api/doctor/assigned_patients")
api.add_resource(DoctorAvailabilityAPI, "/api/doctor/availability")

# Patient
api.add_resource(PatientProfileAPI, "/api/patient/profile")
api.add_resource(PatientAppointmentsAPI, "/api/patient/appointments", "/api/patient/appointments/<int:appointment_id>")
api.add_resource(DepartmentDoctorsAPI, "/api/departments/<int:department_id>/doctors")
api.add_resource(DoctorProfilePatientViewAPI, "/api/doctors/<int:doctor_id>")
api.add_resource(PatientBookAppointmentAPI, "/api/patient/book_appointment")
api.add_resource(PatientHistoryExportCSVAPI, "/api/patient/history/export_csv") # Direct download
api.add_resource(PaymentAPI, "/api/patient/pay/<int:appointment_id>")
api.add_resource(ExportPatientHistoryAPI, "/api/patient/history/export") # Async Email export
api.add_resource(PatientViewDoctorAvailabilityAPI, "/api/patient/doctor_availability/<int:doctor_id>")

@app.route("/")
def home():
    return "Hello, Flask! Your server is working."

if __name__ == "__main__":
    db.create_all()
    add_admin()
    app.run(debug=True)