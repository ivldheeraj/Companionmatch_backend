from flask import request, jsonify
from models.user_models import UserRegisterModel, AddressModel, UserLoginModel
from services.implementations.auth_service import AuthService

auth_service = AuthService()

def register_auth_routes(app):
    @app.route("/register", methods=["POST"])
    def register():
        try:
            data = request.get_json()
            address = AddressModel(**data["address"])
            user_data = UserRegisterModel(
                email=data["email"],
                password=data["password"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                address=address,
                student_bio=data["student_bio"]
            )
            result = auth_service.register_student(user_data)
            return jsonify(result), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/login", methods=["POST"])
    def login():
        try:
            data = request.get_json()
            login_model = UserLoginModel(**data)
            result = auth_service.authenticate_user(login_model)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 401
