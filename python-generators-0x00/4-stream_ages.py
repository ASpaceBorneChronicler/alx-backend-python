#!/usr/bin/python3
import mysql.connector

# This line assumes a 'seed' module exists with a 'connect_to_prodev' function.
# You would need to ensure 'seed.py' is in the same directory and is functional.
try:
    seed = __import__('seed')
except ImportError:
    print("Warning: 'seed.py' module not found. Assuming connection details.")
    # Fallback for demonstration if seed.py is not available
    class MockSeed:
        def connect_to_prodev(self):
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ALX_prodev"
            )
    seed = MockSeed()

def stream_user_ages():
    """
    A generator that streams user ages one by one from the 'user_data' table.
    """
    connection = None
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT age FROM user_data")
        
        # Loop 1: This loop iterates over the cursor to fetch ages one by one
        for (age,) in cursor:
            yield age

    except mysql.connector.Error as err:
        print(f"Error streaming user ages: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()

def calculate_average_age():
    """
    Calculates the average age of users without loading the entire dataset into memory.
    """
    total_age = 0
    count = 0
    
    # Loop 2: This loop consumes the generator, fetching one age at a time
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No user data found to calculate the average age.")

if __name__ == '__main__':
    calculate_average_age()