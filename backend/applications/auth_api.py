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

ALLOWED_REGISTRATION_ROLES = ["Doctor", "Patient"]
ALLOWED_ROLES = ["Admin", "Doctor", "Patient"]


class LoginAPI(Resource):
    def post(self):
        data = request.json

        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return {"message": "Both email and password are required"}, 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "User not found"}, 404

        if user.role not in ALLOWED_ROLES:
            return {"message": "Invalid user role"}, 400

        if user.password != password:
            return {"message": "Incorrect Password"}, 400

        token = create_access_token(
            identity=user.user_id, additional_claims={"role": user.role}
        )
        return {
            "message": f"{user.name} ({user.role}) logged in successfully.",
            "token": token,
        }, 200


class SignUpAPI(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        role = data.get("role", "Patient")

        if not email or not data.get("password") or not data.get("name") or not role:
            return {
                "message": "Name, email, role and password are required for successful signup"
            }, 400

        if len(data.get("name").strip()) > 100 or len(data.get("name").strip()) < 4:
            return {
                "message": "Name should be in between 4 and 100 characters long"
            }, 400

        if len(data.get("email").strip()) > 120 or "@" not in data.get("email").strip():
            return {
                "message": "Email should not be more than 120 characters and must contain an @"
            }, 400

        if (
            len(data.get("password").strip()) > 20
            or len(data.get("password").strip()) < 8
        ):
            return {
                "message": "Password should be between 8 and 20 characters long"
            }, 400

        if len(data.get("phone", "").strip()) > 10:
            return {"message": "Phone number should not be more than 10 numbers"}, 400

        try:
            datetime.strptime(data.get("date_of_birth", "").strip(), "%d-%m-%Y")
        except ValueError:
            return {"message": "Date of Birth should be in dd-mm-yyyy format"}, 400

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
            password=data.get("password"),
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

        return {"message": f"{user.name} ({user.role}) signed in successfully."}, 201
