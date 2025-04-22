from repositories.implementations.match_repository import MatchRepository
from exceptions.custom_exceptions import NotFoundException, ConflictException

class MatchService:
    def __init__(self):
        self.repo = MatchRepository()

    def fetch_matched_profiles(self, student_id, event_id):
        results = self.repo.get_matched_students(student_id, event_id)
        if not results:
            raise NotFoundException("No matches found.")
        return results

    def send_request(self, sender_id, requestor_id):
        if sender_id == requestor_id:
            raise ConflictException("Cannot send request to yourself.")
        self.repo.create_match_request(sender_id, requestor_id)

    def view_incoming_requests(self, requestor_id):
        return self.repo.get_incoming_requests(requestor_id)

    def respond_to_request(self, match_id, status):
        if status not in [2, 3]:
            raise ConflictException("Invalid status. Use 2 (accept) or 3 (reject).")
        self.repo.update_request_status(match_id, status)
