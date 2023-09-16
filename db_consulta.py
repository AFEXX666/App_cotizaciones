import mysql.connector

def get_database_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='cot_app'
        )
    except mysql.connector.Error as e:
        print("Error de MariaDB:", e)
    finally:
        return conn

