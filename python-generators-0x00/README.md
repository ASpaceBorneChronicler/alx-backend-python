# Python Generators and MySQL Database

This project demonstrates the use of a Python generator to stream data from a MySQL database one row at a time, which is highly efficient for handling large datasets.

## Setup

1.  **Install MySQL Connector:**
    ```sh
    pip install mysql-connector-python
    ```
2.  **Ensure MySQL is running** on `localhost`.
3.  **Create an empty CSV file** named `user_data.csv` in the same directory and populate it with your sample data.
4.  **Create the `seed.py` file** and copy the provided code into it.
5.  **Create the `0-main.py` file** and copy the provided code into it.

## File Descriptions

* `seed.py`: This script contains the functions to connect to a MySQL database, create a database and table, and populate the table with data from a CSV file. It also includes the `stream_database_rows` generator function.

* `0-main.py`: This script demonstrates how to use the functions in `seed.py` to set up the database and insert data. It also shows how to call and use the `stream_database_rows` generator to process the data efficiently.

## Usage

To set up the database and see the generator in action, run the main script from your terminal:

```sh
./0-main.py