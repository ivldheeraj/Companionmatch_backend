from dataclasses import dataclass

class MatchedStudentResponse:
    def __init__(self, student_id, first_name, last_name, bio, match_score):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.match_score = match_score

class MatchActionModel:
    def __init__(self, sender_id: int, requestor_id: int):
        self.sender_id = sender_id
        self.requestor_id = requestor_id

class MatchStatusUpdateModel:
    def __init__(self, match_id: int, status: int):
        self.match_id = match_id
        self.status = status
