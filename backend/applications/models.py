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

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # Common
    email = Column(String(120), unique=True, nullable=False)  # Common
    password_hash = Column(String(255), nullable=False)  # Common
    phone = Column(String(20))  # Common
    gender = Column(String(10))  # Common
    date_of_birth = Column(String(10))  # Common

    # Patient-specific fields
    address = Column(Text)  # Patient
    emergency_contact = Column(String(20))  # Patient
    blood_group = Column(String(5))  # Patient

    # Doctor-specific fields
    experience_years = Column(Integer)  # Doctor
    qualification = Column(String(255))  # Doctor
    status = Column(String(20), default="Active")  # Doctor

    # Role field (decides whether this is Admin, Doctor, or Patient)
    role = Column(Enum("Admin", "Doctor", "Patient", name="user_roles"), nullable=False)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    doctor_department = relationship(
        "Department", back_populates="head_doctor", uselist=False
    )
    doctor_appointments = relationship(
        "Appointment",
        back_populates="doctor",
        foreign_keys="Appointment.doctor_id",
        cascade="all, delete-orphan",
    )
    patient_appointments = relationship(
        "Appointment",
        back_populates="patient",
        foreign_keys="Appointment.patient_id",
        cascade="all, delete-orphan",
    )


class Department(db.Model):
    __tablename__ = "department"

    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    head_doctor_id = Column(Integer, ForeignKey("user.user_id"), nullable=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    head_doctor = relationship("User", back_populates="doctor_department")


class Appointment(db.Model):
    __tablename__ = "appointment"

    appointment_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
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

    # Links back to User with role checks handled in app logic
    patient = relationship(
        "User", back_populates="patient_appointments", foreign_keys=[patient_id]
    )
    doctor = relationship(
        "User", back_populates="doctor_appointments", foreign_keys=[doctor_id]
    )
    treatment = relationship(
        "Treatment",
        back_populates="appointment",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Treatment(db.Model):
    __tablename__ = "treatment"

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

    appointment = relationship("Appointment", back_populates="treatment")
