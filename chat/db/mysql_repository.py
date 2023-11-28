import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = os.getenv('DB_PASSWORD'),
            database = "movistar"
        )
        return connection
    except mysql.connector.errors as e:
        print("Error al conectar a MySQL", e)
        return None