from db_config.db_config import get_connection

class QuestionnaireRepository:
    def fetch_all_questionnaires(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Fetch all questionnaires
            cursor.execute("SELECT * FROM QUESTIONNAIRE")
            questionnaires = cursor.fetchall()

            # For each questionnaire, get its questions
            for q in questionnaires:
                cursor.execute("""
                    SELECT qu.QuestionID, qu.Question
                    FROM QUESTION qu
                    JOIN QUESTIONQUESTIONNARIE qq ON qu.QuestionID = qq.QuestionID
                    WHERE qq.QuestionnaireID = %s
                """, (q["QuestionnaireID"],))
                questions = cursor.fetchall()

                for question in questions:
                    cursor.execute("""
                        SELECT OptionID, OptionText
                        FROM ANSWEROPTION
                        WHERE QuestionID = %s
                    """, (question["QuestionID"],))
                    options = cursor.fetchall()
                    question["Options"] = options

                q["Questions"] = questions

            return questionnaires

        except Exception as e:
            raise Exception(f"Repository Error: {e}")
        finally:
            try:
                if cursor: cursor.close()
                if conn: conn.close()
            except:
                pass

    def fetch_questionnaire_list(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT QuestionnaireID, Description FROM QUESTIONNAIRE")
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Repository Error: {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def fetch_questionnaire_by_id(self, questionnaire_id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM QUESTIONNAIRE WHERE QuestionnaireID = %s", (questionnaire_id,))
            questionnaire = cursor.fetchone()
            if not questionnaire:
                raise Exception("Questionnaire not found")

            cursor.execute("""
                SELECT qu.QuestionID, qu.Question
                FROM QUESTION qu
                JOIN QUESTIONQUESTIONNARIE qq ON qu.QuestionID = qq.QuestionID
                WHERE qq.QuestionnaireID = %s
            """, (questionnaire_id,))
            questions = cursor.fetchall()

            for question in questions:
                cursor.execute("""
                    SELECT OptionID, OptionText
                    FROM ANSWEROPTION
                    WHERE QuestionID = %s
                """, (question["QuestionID"],))
                question["Options"] = cursor.fetchall()

            questionnaire["Questions"] = questions
            return questionnaire

        except Exception as e:
            raise Exception(f"Repository Error: {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
