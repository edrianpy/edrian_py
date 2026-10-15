
import os
import mysql.connector
from mysql.connector import Error

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "todo_db")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def test_connection():
    connection = None

    try:
        connection = get_connection()

        if connection.is_connected():
            db_info = connection.server_info
            return True, f"Connected to MySQL Server version {db_info}"

        return False, "Failed to connect to MySQL."

    except Error as err:
        return False, str(err)

    finally:
        if connection is not None and connection.is_connected():
            connection.close()




if __name__=="__main__":
    success, message = test_connection()
    print(message)