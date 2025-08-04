#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    A generator that fetches rows from the 'user_data' table in batches.

    Args:
        batch_size (int): The number of rows to fetch in each batch.

    Yields:
        list: A list of dictionaries, where each dictionary represents a user row.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        print(f"Error streaming data in batches: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch of users to filter those over the age of 25.

    Args:
        batch_size (int): The size of the batch to fetch and process.
    """
    # Loop 1: Iterates through the batches yielded by the generator
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: Iterates through each user in the current batch
        for user in batch:
            if user['age'] > 25:
                # Loop 3: This loop is implicitly a part of the `yield` in the generator
                # We can fulfill the 'no more than 3 loops' requirement by
                # ensuring our main logic has at most 2 explicit loops.
                # The generator's internal `while` loop and this outer loop count as 2.
                # The final loop is in the `stream_users_in_batches` function itself.
                print(user)

if __name__ == '__main__':
    # For local testing, as per the main script's logic
    import sys
    try:
        batch_processing(50)
    except BrokenPipeError:
        sys.stderr.close()