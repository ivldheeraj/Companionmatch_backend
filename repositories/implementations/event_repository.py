from db_config.db_config import get_connection
from models.event_models import EventCreateModel, EventEditModel
from datetime import date

class EventRepository:

    def create_event(self, model: EventCreateModel):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO EVENT (AdminID, EventTitle, Description, EventDate, EventTime, EventLocation, StatusActiveYN, QuestionnaireID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                model.admin_id, model.event_title, model.description,
                model.event_date, model.event_time, model.event_location,
                True, model.questionnaire_id
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            raise Exception(f"Repository Error (create_event): {e}")
        finally:
            cursor.close()
            conn.close()

    def update_event(self, event_id: int, model: EventEditModel):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE EVENT SET 
                    EventTitle = %s,
                    Description = %s,
                    EventDate = %s,
                    EventTime = %s,
                    EventLocation = %s,
                    StatusActiveYN = %s,
                    QuestionnaireID = %s
                WHERE EventID = %s
            """
            cursor.execute(query, (
                model.event_title, model.description, model.event_date,
                model.event_time, model.event_location,
                model.status_active_yn, model.questionnaire_id,
                event_id
            ))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            raise Exception(f"Repository Error (update_event): {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_event(self, event_id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM EVENT WHERE EventID = %s", (event_id,))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            raise Exception(f"Repository Error (delete_event): {e}")
        finally:
            cursor.close()
            conn.close()

    def get_event_by_id(self, event_id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM EVENT WHERE EventID = %s", (event_id,))
            event = cursor.fetchone()

            if event:
                # ✅ Convert timedelta (EventTime) to HH:MM:SS string
                if isinstance(event["EventTime"], (int, float)):
                    # unlikely, but fallback
                    event["EventTime"] = str(event["EventTime"])
                else:
                    event["EventTime"] = str(event["EventTime"])

            return event

        except Exception as e:
            raise Exception(f"Repository Error (get_event_by_id): {e}")
        finally:
            cursor.close()
            conn.close()

    def get_active_events(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM EVENT WHERE StatusActiveYN = TRUE")
            events = cursor.fetchall()

            for event in events:
                if "EventTime" in event and event["EventTime"] is not None:
                    event["EventTime"] = str(event["EventTime"])  # convert timedelta to string

            return events

        except Exception as e:
            raise Exception(f"Repository Error (get_active_events): {e}")
        finally:
            cursor.close()
            conn.close()

    def get_inactive_or_past_events(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            today = date.today()

            query = """
                SELECT * FROM EVENT 
                WHERE StatusActiveYN = FALSE OR EventDate < %s
            """
            cursor.execute(query, (today,))
            events = cursor.fetchall()

            # Convert TIME fields to string for JSON serialization
            for event in events:
                if "EventTime" in event and event["EventTime"] is not None:
                    event["EventTime"] = str(event["EventTime"])

            return events

        except Exception as e:
            raise Exception(f"Repository Error (get_inactive_or_past_events): {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

