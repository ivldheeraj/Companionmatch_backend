from models.event_registration_model import EventRegistrationModel
from repositories.implementations.student_repository import StudentRepository

class StudentService:
    def __init__(self):
        self.repo = StudentRepository()

    def register_event(self, model: EventRegistrationModel):
        try:
            return self.repo.register_event_with_responses(model)
        except Exception as e:
            raise Exception(f"Service Error (register_event): {e}")

    def get_non_registered_events(self, student_id: int, active_only: bool = True):
        try:
            return self.repo.get_active_events_with_registration_flag(student_id)
        except Exception as e:
            raise Exception(f"Service Error (get_non_registered_events): {e}")
