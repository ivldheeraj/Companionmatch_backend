from repositories.implementations.event_repository import EventRepository
from models.event_models import EventCreateModel, EventEditModel

class EventService:
    def __init__(self):
        self.repo = EventRepository()

    def create_event(self, model: EventCreateModel):
        try:
            return self.repo.create_event(model)
        except Exception as e:
            raise Exception(f"Service Error (create_event): {e}")

    def edit_event(self, event_id: int, model: EventEditModel):
        try:
            return self.repo.update_event(event_id, model)
        except Exception as e:
            raise Exception(f"Service Error (edit_event): {e}")

    def delete_event(self, event_id: int):
        try:
            return self.repo.delete_event(event_id)
        except Exception as e:
            raise Exception(f"Service Error (delete_event): {e}")

    def get_active_events(self):
        try:
            return self.repo.get_active_events()
        except Exception as e:
            raise Exception(f"Service Error (get_active_events): {e}")

    def get_event_by_id(self, event_id: int):
        try:
            event = self.repo.get_event_by_id(event_id)
            if not event:
                raise Exception("Event not found")
            return event
        except Exception as e:
            raise Exception(f"Service Error (get_event_by_id): {e}")

    def get_inactive_or_past_events(self):
        try:
            return self.repo.get_inactive_or_past_events()
        except Exception as e:
            raise Exception(f"Service Error (get_inactive_or_past_events): {e}")
