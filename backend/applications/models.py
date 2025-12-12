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
    Float,
    Boolean,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    phone = Column(String(10))
    gender = Column(String(10))
    date_of_birth = Column(Date)
    address = Column(Text)
    emergency_contact = Column(String(20))
    blood_group = Column(String(3))
    experience_years = Column(Integer)
    qualification = Column(String(255))
    status = Column(String(20), default="Active")
    role = Column(Enum("Admin", "Doctor", "Patient", name="user_roles"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    doctor_department = relationship(
        "Department",
        back_populates="head_doctor",
        uselist=False,
        foreign_keys="[Department.head_doctor_id]",
    )

    department_id = Column(
        Integer, ForeignKey("department.department_id"), nullable=True
    )
    department = relationship(
        "Department", back_populates="doctors", foreign_keys=[department_id]
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

    head_doctor = relationship(
        "User", back_populates="doctor_department", foreign_keys=[head_doctor_id]
    )
    doctors = relationship(
        "User", back_populates="department", foreign_keys="[User.department_id]"
    )


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
    payment_status = Column(
        Enum("Paid", "Unpaid", "Pending", name="payment_status"), default="Unpaid"
    )
    fee_amount = Column(Float, nullable=True)

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


class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availability'

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    date = Column(Date, nullable=False)
    available_morning = Column(Boolean, default=True) # 08:00 - 12:00
    available_evening = Column(Boolean, default=True) # 16:00 - 21:00

    __table_args__ = (UniqueConstraint('doctor_id', 'date', name='_doctor_date_uc'),)