import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nandita@1805",
            database="movie"
        )
        print("Connection successful!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
