from flask import Flask, request
from flask_restful import Api
from applications.models import db, User
from applications.api import WelcomeAPI, LoginAPI, SignUpAPI
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    base_dir, "database.sqlite3"
)

db.init_app(app)
api = Api(app)
app.app_context().push()


def add_admin():
    admin = User.query.filter(
        (User.name == "Admin") | (User.email == "admin@gmail.com")
    ).first()
    if not admin:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password_hash="1234",
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


@app.route("/")
def home():
    return "Hello World!"


if __name__ == "__main__":
    db.create_all()
    add_admin()
    app.run(debug=True)
