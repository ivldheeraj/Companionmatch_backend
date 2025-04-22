from db_config.db_config import get_connection
from models.event_registration_model import EventRegistrationModel
from datetime import date


class StudentRepository:
    def insert_student(self, student_id: int, student_bio: str):
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO STUDENT (StudentID, StudentBio) VALUES (%s, %s)"
        cursor.execute(query, (student_id, student_bio))
        conn.commit()
        cursor.close()
        conn.close()

    def register_event_with_responses(self, model: EventRegistrationModel):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            today = date.today()

            # Step 1: Insert registration
            cursor.execute("""
                INSERT INTO EVENTREGISTRATION (StudentID, EventID, RegistrationDate)
                VALUES (%s, %s, %s)
            """, (model.student_id, model.event_id, today))
            registration_id = cursor.lastrowid

            # Step 2: Insert responses
            for response in model.responses:
                cursor.execute("""
                    INSERT INTO STUDENTRESPONSE (OptionID, RegistrationID)
                    VALUES (%s, %s)
                """, (response.option_id, registration_id))

            conn.commit()
            return registration_id
        except Exception as e:
            conn.rollback()
            raise Exception(f"Repository Error (register_event_with_responses): {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_active_events_with_registration_flag(self, student_id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Step 1: Get all active events
            cursor.execute("""
                SELECT *
                FROM EVENT
                WHERE StatusActiveYN = TRUE
            """)
            events = cursor.fetchall()

            if not events:
                return []

            # Step 2: Get all registered event IDs for the student
            cursor.execute("""
                SELECT EventID
                FROM EVENTREGISTRATION
                WHERE StudentID = %s
            """, (student_id,))
            registered_ids = {row["EventID"] for row in cursor.fetchall()}

            # Step 3: Add registration flag
            for event in events:
                event["isStudentRegistered"] = event["EventID"] in registered_ids

                # Format time field for JSON
                if "EventTime" in event and event["EventTime"]:
                    event["EventTime"] = str(event["EventTime"])

            return events

        except Exception as e:
            raise Exception(f"Repository Error (get_active_events_with_registration_flag): {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()