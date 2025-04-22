from controllers.implementations.auth_controller import register_auth_routes
from controllers.implementations.event_controller import register_event_routes
from controllers.implementations.match_controller import register_match_routes
from controllers.implementations.questionnaire_controller import register_questionnaire_routes
from controllers.implementations.student_controller import register_student_routes


def register_all_routes(app):
    register_auth_routes(app)
    register_questionnaire_routes(app)
    register_event_routes(app)
    register_student_routes(app)
    register_match_routes(app)
