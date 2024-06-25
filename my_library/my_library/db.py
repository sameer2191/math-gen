# my_library/db.py
import mysql.connector
from mysql.connector import Error
import logging

def initialize_database(config):
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password']
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS openai_questions")
            cursor.execute("USE openai_questions")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS qa_sessions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    question TEXT NOT NULL,
                    response TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Database and table ensured")
    except Error as e:
        logging.error(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
