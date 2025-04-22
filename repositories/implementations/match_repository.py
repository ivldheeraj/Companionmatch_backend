from db_config.db_config import get_connection
from exceptions.custom_exceptions import DatabaseException

class MatchRepository:
    def get_matched_students(self, current_student_id: int, event_id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # 1. Fetch current student's selected options for this event
            cursor.execute("""
                SELECT OptionID
                FROM STUDENTRESPONSE sr
                JOIN EVENTREGISTRATION er ON sr.RegistrationID = er.RegistrationID
                WHERE er.StudentID = %s AND er.EventID = %s
            """, (current_student_id, event_id))
            my_options = set(row["OptionID"] for row in cursor.fetchall())

            if not my_options:
                return []

            # 2. Fetch other students’ responses in the same event
            cursor.execute("""
                SELECT er.StudentID, sr.OptionID
                FROM STUDENTRESPONSE sr
                JOIN EVENTREGISTRATION er ON sr.RegistrationID = er.RegistrationID
                WHERE er.EventID = %s AND er.StudentID != %s
            """, (event_id, current_student_id))

            match_map = {}
            for row in cursor.fetchall():
                sid = row["StudentID"]
                match_map.setdefault(sid, set()).add(row["OptionID"])

            matched_students = []
            for sid, options in match_map.items():
                score = len(my_options.intersection(options))
                if score >= 3:
                    # Fetch student profile
                    cursor.execute("""
                        SELECT u.UserID, u.FirstName, u.LastName, s.StudentBio
                        FROM USER u
                        JOIN STUDENT s ON s.StudentID = u.UserID
                        WHERE u.UserID = %s
                    """, (sid,))
                    student_info = cursor.fetchone()
                    student_info["MatchScore"] = score

                    # Fetch status from COMPANIONMATCH (if any)
                    cursor.execute("""
                        SELECT StatusAcceptYN
                        FROM COMPANIONMATCH
                        WHERE SenderID = %s AND RequestorID = %s
                    """, (current_student_id, sid))
                    status_row = cursor.fetchone()
                    student_info["StatusAcceptYN"] = status_row["StatusAcceptYN"] if status_row else 0

                    matched_students.append(student_info)

            return matched_students

        except Exception as e:
            raise DatabaseException(str(e))

    def create_match_request(self, sender_id, requestor_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO COMPANIONMATCH (RequestorID, SenderID, StatusAcceptYN, MatchScore, ResponseID)
                VALUES (%s, %s, 1, 3, 1)
            """, (requestor_id, sender_id))  # Static score/response for now
            conn.commit()
        except Exception as e:
            raise DatabaseException(str(e))

    def get_incoming_requests(self, requestor_id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT 
                    cm.MatchID,
                    cm.SenderID,
                    cm.StatusAcceptYN,
                    u.FirstName,
                    u.LastName,
                    s.StudentBio
                FROM COMPANIONMATCH cm
                JOIN USER u ON u.UserID = cm.SenderID
                JOIN STUDENT s ON s.StudentID = u.UserID
                WHERE cm.RequestorID = %s
            """, (requestor_id,))

            return cursor.fetchall()

        except Exception as e:
            raise DatabaseException(str(e))

    def update_request_status(self, match_id, status):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE COMPANIONMATCH SET StatusAcceptYN = %s WHERE MatchID = %s
            """, (status, match_id))
            conn.commit()
        except Exception as e:
            raise DatabaseException(str(e))
