import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# ✅ Database connection using .env
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# ✅ Seed Questionnaires with 5 categories, 25 questions, 100 options
def seed_questionnaires():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Master questionnaire data
        questionnaires = {
            "Sports": [
                ("What's your favorite sport?", ["Football", "Basketball", "Tennis", "Cricket"]),
                ("How often do you play sports?", ["Daily", "Weekly", "Occasionally", "Never"]),
                ("Do you enjoy watching sports events?", ["Yes", "Sometimes", "Rarely", "No"]),
                ("Preferred sports location?", ["Stadium", "Gym", "Ground", "TV at Home"]),
                ("Team or Individual sports?", ["Team", "Individual", "Both", "None"])
            ],
            "Seminars": [
                ("Do you like attending seminars?", ["Yes", "Sometimes", "Rarely", "No"]),
                ("What type of seminars interest you?", ["Technical", "Career", "Motivational", "Others"]),
                ("Preferred seminar timing?", ["Morning", "Afternoon", "Evening", "No Preference"]),
                ("Do you prefer online or offline?", ["Online", "Offline", "Hybrid", "Doesn’t matter"]),
                ("Would you speak in a seminar?", ["Yes", "Maybe", "Never", "Depends"])
            ],
            "Health Related Events": [
                ("Do you attend health camps?", ["Yes", "No", "Sometimes", "Never"]),
                ("Do you follow a fitness routine?", ["Yes", "Occasionally", "Trying to", "Not at all"]),
                ("Preferred health events?", ["Yoga", "Checkup", "Diet Seminar", "Mental Wellness"]),
                ("Do you have any allergies?", ["Yes", "No", "Not Sure", "Prefer Not to Say"]),
                ("How important is health to you?", ["Very", "Important", "Somewhat", "Not Much"])
            ],
            "Tech Workshops": [
                ("Preferred tech domain?", ["AI", "Web Dev", "Cloud", "Data Science"]),
                ("Do you attend coding bootcamps?", ["Yes", "Sometimes", "No", "Planning to"]),
                ("What motivates you to attend?", ["Knowledge", "Networking", "Certificate", "Curiosity"]),
                ("How do you prefer learning?", ["Hands-on", "Lectures", "Projects", "Self-study"]),
                ("Any prior workshop experience?", ["Yes", "Few", "Newbie", "None"])
            ],
            "Other Common Events": [
                ("Do you prefer indoor or outdoor events?", ["Indoor", "Outdoor", "Both", "None"]),
                ("Do you enjoy cultural events?", ["Yes", "No", "Sometimes", "Never attended"]),
                ("Preferred music type?", ["Classical", "Pop", "Rock", "No Preference"]),
                ("What’s your weekend activity?", ["Reading", "Party", "Sports", "Netflix"]),
                ("Would you travel for an event?", ["Yes", "Depends", "No", "Maybe"])
            ]
        }

        # Loop and insert into DB
        for title, questions in questionnaires.items():
            cursor.execute("INSERT INTO QUESTIONNAIRE (Description) VALUES (%s)", (title,))
            questionnaire_id = cursor.lastrowid

            for question_text, options in questions:
                cursor.execute("INSERT INTO QUESTION (Question) VALUES (%s)", (question_text,))
                question_id = cursor.lastrowid

                # ✅ Corrected column name: QuestionnaireID (not QuestionnarieID)
                cursor.execute(
                    "INSERT INTO QUESTIONQUESTIONNARIE (QuestionnaireID, QuestionID) VALUES (%s, %s)",
                    (questionnaire_id, question_id)
                )

                for opt in options:
                    cursor.execute(
                        "INSERT INTO ANSWEROPTION (QuestionID, OptionText) VALUES (%s, %s)",
                        (question_id, opt)
                    )

        conn.commit()
        print("✅ Seeded 5 questionnaires with 25 questions and 100 options total.")

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
    finally:
        try:
            if cursor: cursor.close()
            if conn: conn.close()
        except:
            pass

# Run the function
if __name__ == "__main__":
    seed_questionnaires()
