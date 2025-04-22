from dataclasses import dataclass
from typing import Optional

@dataclass
class EventCreateModel:
    event_title: str
    description: str
    event_date: str
    event_time: str
    event_location: str
    questionnaire_id: int
    admin_id: int

@dataclass
class EventEditModel:
    event_title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[str] = None
    event_time: Optional[str] = None
    event_location: Optional[str] = None
    questionnaire_id: Optional[int] = None
    status_active_yn: Optional[bool] = None

@dataclass
class EventResponseModel:
    event_id: int
    event_title: str
    description: str
    event_date: str
    event_time: str
    event_location: str
    questionnaire_id: int
    admin_id: int
    status_active_yn: bool
