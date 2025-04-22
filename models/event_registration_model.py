from dataclasses import dataclass
from typing import List

@dataclass
class ResponseModel:
    option_id: int

@dataclass
class EventRegistrationModel:
    student_id: int
    event_id: int
    responses: List[ResponseModel]
