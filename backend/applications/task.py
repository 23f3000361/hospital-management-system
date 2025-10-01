from flask import current_app
from datetime import date, datetime
from sqlalchemy import extract
from .models import Appointment, Treatment, User
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import csv
import io
from .worker import celery
from celery.schedules import crontab
from sqlalchemy.orm import joinedload
from email import encoders


@celery.task
def send_daily_reminders():
    with current_app.app_context():
        today = date.today()
        appointments = Appointment.query.filter_by(date=today, status="Booked").all()

        for appt in appointments:
            patient = User.query.get(appt.patient_id)

            if patient and patient.email:
                message = f"Hello {patient.name},\n\nThis is a reminder for your appointment at the hospital today at {appt.time}. Please be on time.\n\nThank you,\nThe Hospital Management Team"

                sender_email = "your_email@example.com"
                password = "your_password"
                subject = "Appointment Reminder"

                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = patient.email
                msg["Subject"] = subject
                msg.attach(MIMEText(message, "plain"))

                try:
                    with smtplib.SMTP("smtp.example.com", 587) as server:
                        server.starttls()  # Secure the connection
                        server.login(sender_email, password)
                        server.send_message(msg)
                    print(f"Daily reminder sent to {patient.name} at {patient.email}")
                except Exception as e:
                    print(f"Failed to send email to {patient.name}: {e}")


@celery.task
def generate_monthly_report():
    with current_app.app_context():
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
            report_html += "<table><thead><tr><th>Date</th><th>Patient</th><th>Diagnosis</th><th>Prescription</th></tr></thead><tbody>"

            for appt in appointments:
                treatment = Treatment.query.filter_by(
                    appointment_id=appt.appointment_id
                ).first()
                patient = User.query.get(appt.patient_id)

                if not patient or not treatment:
                    continue

                diagnosis = treatment.diagnosis if treatment else "N/A"
                prescription = treatment.prescription if treatment else "N/A"

                report_html += f"<tr><td>{appt.date}</td><td>{patient.name}</td><td>{diagnosis}</td><td>{prescription}</td></tr>"

            report_html += "</tbody></table>"

            if doctor.email:
                msg = MIMEMultipart()
                msg["From"] = "your_email@example.com"
                msg["To"] = doctor.email
                msg["Subject"] = f"Monthly Report for {today.strftime('%B %Y')}"
                msg.attach(MIMEText(report_html, "html"))

                try:
                    with smtplib.SMTP("smtp.example.com", 587) as server:
                        server.starttls()
                        server.login("your_email@example.com", "your_password")
                        server.send_message(msg)
                    print(f"Monthly report sent to {doctor.name}")
                except Exception as e:
                    print(f"Failed to send email to {doctor.name}: {e}")


@celery.task
def export_patient_history_csv(patient_id):
    with current_app.app_context():
        patient = User.query.filter_by(user_id=patient_id, role="Patient").first()
        if not patient:
            return {"message": "Patient not found"}, 404

        # Query all appointments with their linked doctor and treatment data
        appointments = (
            Appointment.query.filter_by(patient_id=patient_id)
            .options(joinedload(Appointment.doctor), joinedload(Appointment.treatment))
            .all()
        )

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "user_id",
                "username",
                "consulting_doctor",
                "appointment_date",
                "diagnosis",
                "prescription",
                "next_visit",
            ]
        )

        for appt in appointments:
            doctor = appt.doctor
            treatment = appt.treatment

            writer.writerow(
                [
                    patient.user_id,
                    patient.name,
                    doctor.name if doctor else "N/A",
                    str(appt.date),
                    treatment.diagnosis if treatment else "N/A",
                    treatment.prescription if treatment else "N/A",
                    (
                        str(treatment.follow_up_date)
                        if treatment and treatment.follow_up_date
                        else "N/A"
                    ),
                ]
            )

        # Prepare the email
        msg = MIMEMultipart()
        msg["From"] = "your_email@example.com"
        msg["To"] = patient.email
        msg["Subject"] = "Your Patient History Export"

        body = "Attached is your requested patient history in CSV format."
        msg.attach(MIMEText(body, "plain"))

        # Attach the CSV file
        filename = f"patient_history_{patient_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        part = MIMEBase("application", "octet-stream")
        part.set_payload(output.getvalue().encode("utf-8"))
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
        msg.attach(part)

        # Send the email
        try:
            with smtplib.SMTP("smtp.example.com", 587) as server:
                server.starttls()
                server.login("your_email@example.com", "your_password")
                server.send_message(msg)
            print(f"CSV report successfully mailed to {patient.email}")
        except Exception as e:
            print(f"Failed to send email with CSV to {patient.email}: {e}")

    return {"message": "CSV export completed and sent via email."}


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=9, minute=0),
        send_daily_reminders.s(),
        name="daily appointment reminders",
    )

    sender.add_periodic_task(
        crontab(day_of_month=1, hour=8, minute=0),
        generate_monthly_report.s(),
        name="monthly doctor activity report",
    )
