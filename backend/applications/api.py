from flask import request, current_app as app
from flask_restful import Resource
from .models import db, User, Appointment, Department, Treatment
from sqlalchemy.orm import joinedload
from flask_caching import Cache
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
    get_jwt,
)
from datetime import datetime, date
import time

ALLOWED_REGISTRATION_ROLES = ["Doctor", "Patient"]
ALLOWED_ROLES = ["Admin", "Doctor", "Patient"]

cache = Cache()


class WelcomeAPI(Resource):
    @jwt_required()
    def get(self):
        print(get_jwt_identity())
        print(get_jwt_identity().get("role"))
        print(get_jwt_identity().get("user_id"))
        return {"message": "Hello, This is the Hospital Management System"}, 200

    def post(self):
        data = request.get_json()
        msg = f'Hello! {data.get("name")}'
        return {"message": msg}, 200
