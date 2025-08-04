#!/usr/bin/python3
import mysql.connector
seed = __import__('seed')

def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the database.

    Args:
        page_size (int): The number of rows to fetch in the page.
        offset (int): The starting position of the page.

    Returns:
        list: A list of dictionaries, where each dictionary represents a user row.
    """
    connection = None
    rows = []
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching page: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()
    return rows

def lazy_paginate(page_size):
    """
    A generator that lazily fetches paginated data from the database.

    Args:
        page_size (int): The number of rows to fetch per page.

    Yields:
        list: A list of dictionaries, representing a page of user data.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

if __name__ == '__main__':
    # This block is for demonstrating the generator locally if needed.
    # The main script '3-main.py' handles the actual execution.
    import sys
    try:
        for page in lazy_paginate(100):
            for user in page:
                print(user)
    except BrokenPipeError:
        sys.stderr.close()