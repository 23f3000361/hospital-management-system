from flask import request
from flask_restful import Resource
from .models import db, User, Appointment, Department, Treatment

ALLOWED_REGISTRATION_ROLES = ["Doctor", "Patient"]
ALLOWED_ROLES = ["Admin", "Doctor", "Patient"]


class WelcomeAPI(Resource):
    def get(self):
        return {"message": "Hello, This is the Hospital Management System"}, 200

    def post(self):
        data = request.get_json()
        msg = f'Hello! {data.get("name")}'
        return {"message": msg}, 200


class LoginAPI(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required"}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User not found"}, 404

        if user.password_hash != password:
            return {"message": "Incorrect Password"}, 400

        if user.role not in ALLOWED_ROLES:
            return {"message": "Invalid user role"}, 400

        return {"message": f"{user.role} {user.name} logged in successfully."}, 200


class SignUpAPI(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        role = data.get("role", "Patient")

        if not email or not data.get("password") or not data.get("name"):
            return {"message": "Name, email, and password are required"}, 400

        user = User.query.filter_by(email=email).first()
        if user:
            return {"message": f"{user.role} already exists"}, 400

        if role not in ALLOWED_REGISTRATION_ROLES:
            return {
                "message": f"Invalid role. Allowed roles for registration are: {ALLOWED_REGISTRATION_ROLES}"
            }, 400

        new_user = User(
            name=data.get("name"),
            email=email,
            password_hash=data.get("password"),
            role=role,
            phone=data.get("phone"),
            gender=data.get("gender"),
            date_of_birth=data.get("date_of_birth"),
            address=data.get("address"),
            emergency_contact=data.get("emergency_contact"),
            blood_group=data.get("blood_group"),
            experience_years=data.get("experience_years"),
            qualification=data.get("qualification"),
        )
        db.session.add(new_user)
        db.session.commit()

        return {
            "message": f"{new_user.role} {new_user.name} signed up successfully."
        }, 201
