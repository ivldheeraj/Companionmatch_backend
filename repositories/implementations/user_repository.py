from db_config.db_config import get_connection
from models.user_models import UserRegisterModel

class UserRepository:
    def insert_user(self, model: UserRegisterModel, user_type: str):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO USER (Email, Password, FirstName, LastName, UserType, StatusActiveYN, AddressID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            model.email, model.password, model.first_name,
            model.last_name, user_type, True, model.address.address_id
        ))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return user_id

    def get_user_by_email(self, email: str):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USER WHERE Email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
