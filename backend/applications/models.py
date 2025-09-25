from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Integer,
    String,
    Column,
    Text,
    Date,
    ForeignKey,
    Enum,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

# Doctor Table, Patient Table, Appointment Table, Treatment Table, Department/Specialization Table
db = SQLAlchemy()


class Admin(db.Model):
    admin_id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    role = Column(String(20), default="Admin")


class Department(db.Model):
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    head_doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    doctors = db.relationship(
        "Doctor",
        back_populates="department",
        cascade="all, delete-orphan",
        foreign_keys="[Doctor.department_id]",
    )

    head_doctor = db.relationship(
        "Doctor", foreign_keys=[head_doctor_id], uselist=False, post_update=True
    )


class Doctor(db.Model):
    doctor_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20))
    gender = Column(String(10))
    date_of_birth = Column(Date)
    department_id = Column(
        Integer, ForeignKey("department.department_id"), nullable=False
    )
    experience_years = Column(Integer)
    qualification = Column(String(255))
    status = Column(String(20), default="Active")
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    department = db.relationship(
        "Department", back_populates="doctors", foreign_keys=[department_id]
    )

    appointments = db.relationship(
        "Appointment", back_populates="doctor", cascade="all, delete-orphan"
    )


class Patient(db.Model):
    patient_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20))
    gender = Column(String(10))
    date_of_birth = Column(Date)
    address = Column(Text)
    emergency_contact = Column(String(20))
    blood_group = Column(String(5))
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    appointments = db.relationship(
        "Appointment", back_populates="patient", cascade="all, delete-orphan"
    )


class Appointment(db.Model):
    appointment_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(String(20), nullable=False)
    status = Column(
        Enum("Booked", "Completed", "Cancelled", name="appointment_status"),
        default="Booked",
    )
    appointment_type = Column(
        Enum("Online", "In-person", name="appointment_type"), default="In-person"
    )
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")
    treatment = db.relationship(
        "Treatment",
        back_populates="appointment",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Treatment(db.Model):
    treatment_id = Column(Integer, primary_key=True)
    appointment_id = Column(
        Integer, ForeignKey("appointment.appointment_id"), nullable=False
    )
    diagnosis = Column(Text)
    prescription = Column(Text)
    notes = Column(Text)
    follow_up_date = Column(Date)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    appointment = db.relationship("Appointment", back_populates="treatment")
