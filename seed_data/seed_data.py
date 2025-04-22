import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def seed_admins():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Insert addresses
        cursor.execute("INSERT INTO ADDRESS VALUES (1, '100 Admin St', 'CityA', 'MI', '48858')")
        cursor.execute("INSERT INTO ADDRESS VALUES (2, '200 Admin Blvd', 'CityB', 'MI', '48958')")

        # Insert admin users
        cursor.execute("""
            INSERT INTO USER (UserID, Email, Password, FirstName, LastName, UserType, StatusActiveYN, AddressID)
            VALUES (101, 'admin1@example.com', 'adminpass1', 'Admin', 'One', 'admin', TRUE, 1)
        """)
        cursor.execute("""
            INSERT INTO USER (UserID, Email, Password, FirstName, LastName, UserType, StatusActiveYN, AddressID)
            VALUES (102, 'admin2@example.com', 'adminpass2', 'Admin', 'Two', 'admin', TRUE, 2)
        """)

        cursor.execute("INSERT INTO ADMIN (AdminID) VALUES (101)")
        cursor.execute("INSERT INTO ADMIN (AdminID) VALUES (102)")

        conn.commit()
        print("✅ Admin data seeded.")
    except Exception as e:
        print("❌ Error during seeding:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_admins()
