from flask import request, jsonify
from models.match_models import MatchActionModel, MatchStatusUpdateModel
from services.implementations.match_service import MatchService
from exceptions.custom_exceptions import NotFoundException, ConflictException

match_service = MatchService()

def register_match_routes(app):
    # ✅ 1. Get Matched Profiles (score >= 3)
    @app.route("/student/matches", methods=["GET"])
    def get_matched_profiles():
        try:
            student_id = int(request.args.get("student_id"))
            event_id = int(request.args.get("event_id"))

            result = match_service.fetch_matched_profiles(student_id, event_id)
            return jsonify(result), 200
        except NotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # ✅ 2. Send Match Request
    @app.route("/student/match/send", methods=["POST"])
    def send_match_request():
        try:
            data = request.get_json()
            model = MatchActionModel(
                sender_id=int(data["sender_id"]),
                requestor_id=int(data["requestor_id"])
            )
            match_service.send_request(model.sender_id,model.requestor_id)
            return jsonify({"message": "Match request sent successfully"}), 201
        except ConflictException as e:
            return jsonify({"error": str(e)}), 409
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # ✅ 3. Get Incoming Requests
    @app.route("/student/match/requests", methods=["GET"])
    def get_incoming_requests():
        try:
            requestor_id = int(request.args.get("requestor_id"))
            result = match_service.view_incoming_requests(requestor_id)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # ✅ 4. Accept or Reject Request
    @app.route("/student/match/respond", methods=["POST"])
    def respond_to_match_request():
        try:
            data = request.get_json()
            model = MatchStatusUpdateModel(
                match_id=int(data["match_id"]),
                status=int(data["status"])
            )
            match_service.respond_to_request(model.match_id, model.status)
            return jsonify({"message": "Match request updated successfully"}), 200
        except ConflictException as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400
