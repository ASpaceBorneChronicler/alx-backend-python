#!/usr/bin/python3
import mysql.connector
import csv
import uuid

def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        print("Connected to MySQL server.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database 'ALX_prodev' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        print("Connected to 'ALX_prodev' database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to 'ALX_prodev': {err}")
        return None

def create_table(connection):
    """Creates the 'user_data' table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(10, 2) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        print("Table 'user_data' created successfully or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def insert_data(connection, file_path):
    """Inserts data from a CSV file into the 'user_data' table."""
    try:
        cursor = connection.cursor()
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                user_id = str(uuid.uuid4())
                name, email, age = row
                try:
                    insert_query = """
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """
                    data = (user_id, name, email, age)
                    cursor.execute(insert_query, data)
                except mysql.connector.Error as err:
                    print(f"Error inserting row {row}: {err}")
        connection.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def stream_database_rows(connection):
    """A generator that streams rows from the 'user_data' table one by one."""
    try:
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

if __name__ == '__main__':
    # This block is for testing purposes, you can use 0-main.py to run the full script
    pass