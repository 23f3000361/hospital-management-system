from email.mime.application import MIMEApplication
from flask import current_app
from datetime import date, datetime
from sqlalchemy import extract
from .models import Appointment, Treatment, User
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv
import io
from .worker import celery
from sqlalchemy.orm import joinedload

# --- MAILHOG CONFIG ---
SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = "admin@hms.com"
# ----------------------


@celery.task
def send_daily_reminders():
    today = date.today()
    appointments = Appointment.query.filter_by(date=today, status="Booked").all()

    if not appointments:
        return "No appointments today."

    for appt in appointments:
        patient = User.query.get(appt.patient_id)

        if patient and patient.email:
            subject = "Appointment Reminder"
            body = f"Hello {patient.name},\n\nThis is a reminder for your appointment today at {appt.time}.\n\nRegards,\nHMS Team"

            send_email(patient.email, subject, body)

    return f"Sent reminders for {len(appointments)} appointments."


@celery.task
def generate_monthly_report():
    today = datetime.now()
    month = today.month
    year = today.year

    doctors = User.query.filter_by(role="Doctor").all()

    for doctor in doctors:
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.user_id,
            extract("month", Appointment.date) == month,
            extract("year", Appointment.date) == year,
        ).all()

        report_html = f"<h1>Monthly Activity Report for Dr. {doctor.name}</h1>"
        report_html += f"<h2>Month: {today.strftime('%B %Y')}</h2>"
        report_html += "<table border='1' cellspacing='0' cellpadding='5'><thead><tr><th>Date</th><th>Patient</th><th>Diagnosis</th></tr></thead><tbody>"

        for appt in appointments:
            patient = appt.patient
            treatment = appt.treatment

            diag = treatment.diagnosis if treatment else "N/A"
            pat_name = patient.name if patient else "Unknown"

            report_html += (
                f"<tr><td>{appt.date}</td><td>{pat_name}</td><td>{diag}</td></tr>"
            )

        report_html += "</tbody></table>"

        if doctor.email:
            send_email(
                doctor.email,
                f"Monthly Report - {today.strftime('%B')}",
                report_html,
                is_html=True,
            )

    return "Monthly reports generated."


@celery.task
def export_patient_history_csv(patient_id):
    patient = User.query.filter_by(user_id=patient_id, role="Patient").first()
    if not patient:
        return "Patient not found"

    appointments = (
        Appointment.query.filter_by(patient_id=patient_id)
        .options(joinedload(Appointment.doctor), joinedload(Appointment.treatment))
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Doctor", "Diagnosis", "Prescription", "Notes"])

    for appt in appointments:
        doc = appt.doctor.name if appt.doctor else "N/A"
        treat = appt.treatment

        diag = treat.diagnosis if treat else "N/A"
        pres = treat.prescription if treat else "N/A"
        notes = treat.notes if treat else "N/A"

        writer.writerow([str(appt.date), doc, diag, pres, notes])

    # Prepare Attachment
    filename = f"history_{patient_id}_{datetime.now().strftime('%Y%m%d')}.csv"

    send_email(
        patient.email,
        "Your Medical History Export",
        "Please find your requested medical history attached.",
        attachment_name=filename,
        attachment_data=output.getvalue(),
    )

    return "CSV Export Completed"


def send_email(
    to_email, subject, body, is_html=False, attachment_name=None, attachment_data=None
):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach Body
    msg.attach(MIMEText(body, "html" if is_html else "plain"))

    # Attach CSV (Using MIMEApplication - More Robust)
    if attachment_name and attachment_data:
        print(
            f"DEBUG: Attaching file '{attachment_name}' with size {len(attachment_data)} bytes"
        )

        # Create the attachment object
        part = MIMEApplication(attachment_data.encode("utf-8"), Name=attachment_name)

        # Add headers to force download behavior
        part["Content-Disposition"] = f'attachment; filename="{attachment_name}"'

        # Attach to message
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)
        print(f"DEBUG: Email sent to {to_email}")
    except Exception as e:
        print(f"ERROR: Failed to send email to {to_email}: {e}")
