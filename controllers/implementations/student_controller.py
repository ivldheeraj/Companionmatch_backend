from flask import request, jsonify

from models.event_registration_model import ResponseModel, EventRegistrationModel
from services.implementations.student_service import StudentService
from datetime import date

student_service = StudentService()

def register_student_routes(app):
    @app.route("/student/register-event", methods=["POST"])
    def register_event():
        try:
            data = request.get_json()

            responses = [ResponseModel(**resp) for resp in data.get("responses", [])]
            model = EventRegistrationModel(
                student_id=data["student_id"],
                event_id=data["event_id"],
                responses=responses
            )

            reg_id = student_service.register_event(model)
            return jsonify({
                "message": "Event registered successfully",
                "registration_id": reg_id,
                "registration_date": str(date.today())
            }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/student/non-registered-events", methods=["GET"])
    def get_non_registered_events():
        try:
            student_id = int(request.args.get("student_id"))
            active_status = request.args.get("active_only", "true").lower() == "true"

            events = student_service.get_non_registered_events(student_id, active_status)
            return jsonify(events), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
