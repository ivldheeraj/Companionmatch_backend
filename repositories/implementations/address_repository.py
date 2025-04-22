from db_config.db_config import get_connection
from models.user_models import AddressModel

class AddressRepository:
    def insert_address(self, model: AddressModel):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO ADDRESS (Street, City, State, Zipcode)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (model.street, model.city, model.state, model.zipcode))
        conn.commit()
        address_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return address_id
