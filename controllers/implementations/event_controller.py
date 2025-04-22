from flask import request, jsonify
from services.implementations.event_service import EventService
from models.event_models import EventCreateModel, EventEditModel

event_service = EventService()

def register_event_routes(app):
    @app.route("/events", methods=["POST"])
    def create_event():
        try:
            data = request.get_json()
            model = EventCreateModel(**data)
            event_id = event_service.create_event(model)
            return jsonify({"message": "Event created", "event_id": event_id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/events/<int:event_id>", methods=["POST"])
    def update_event(event_id):
        try:
            data = request.get_json()
            model = EventEditModel(**data)
            updated = event_service.edit_event(event_id, model)
            if updated:
                return jsonify({"message": "Event updated"}), 200
            return jsonify({"message": "No changes made"}), 204
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/events/<int:event_id>", methods=["DELETE"])
    def delete_event(event_id):
        try:
            deleted = event_service.delete_event(event_id)
            if deleted:
                return jsonify({"message": "Event deleted"}), 200
            return jsonify({"message": "Event not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/events/active", methods=["GET"])
    def get_active_events():
        try:
            events = event_service.get_active_events()
            return jsonify(events), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/events/<int:event_id>", methods=["GET"])
    def get_event_by_id(event_id):
        try:
            event = event_service.get_event_by_id(event_id)
            return jsonify(event), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    @app.route("/events/inactive", methods=["GET"])
    def get_inactive_or_past_events():
        try:
            events = event_service.get_inactive_or_past_events()
            return jsonify(events), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
