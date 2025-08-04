#!/usr/bin/python3
import mysql.connector
import os

def stream_users():
    """
    A generator that streams rows from the 'user_data' table one by one.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        # The loop iterates over the cursor, which fetches rows one by one
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    # This block is for demonstrating the generator locally if needed
    from itertools import islice
    for user in islice(stream_users(), 6):
        print(user)