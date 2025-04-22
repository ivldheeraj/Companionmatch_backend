from flask import jsonify
from services.implementations.questionnaire_service import QuestionnaireService

questionnaire_service = QuestionnaireService()

def register_questionnaire_routes(app):
    @app.route("/questionnaires", methods=["GET"])
    def get_all_questionnaires():
        try:
            result = questionnaire_service.get_all_questionnaires()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/questionnaires/list", methods=["GET"])
    def get_questionnaire_list():
        try:
            result = questionnaire_service.get_questionnaire_list()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/questionnaires/<int:questionnaire_id>", methods=["GET"])
    def get_questionnaire_by_id(questionnaire_id):
        try:
            result = questionnaire_service.get_questionnaire_by_id(questionnaire_id)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500