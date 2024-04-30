from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable


# query to create database
CREATE_DB = """
    CREATE DATABASE message_server_db;
"""

# query to create users table
CREATE_USERS_TABLE = """
    CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(80)
);
"""

# query to create messages table
CREATE_MESSAGES_TABLE = """
    CREATE TABLE messages (
    id SERIAL,
    from_id INT REFERENCES users(id) ON DELETE CASCADE,
    to_user_id INT REFERENCES users(id) ON DELETE CASCADE,
    text VARCHAR(255),  
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

settings = {
    'database': 'message_server_db',
    'user': 'postgres',
    'password': 'coderslab',
    'host': 'localhost',
    'port': 5432,
}

# connection to server and creating database message_server_db with error handling
try:
    connection = connect(
        host=settings['host'],
        user=settings['user'],
        password=settings['password'],
        port=settings['port']
    )
    connection.autocommit = True
    cursor = connection.cursor()

    try:
        cursor.execute(CREATE_DB)
        print("Database created successfully")
    except DuplicateDatabase as e:
        print(f"Database already exists: {e}")
    cursor.close()
    connection.close()

except OperationalError as e:
    print(f"Error: {e}")

# connection to server and creating users table with error handling
try:
    connection = connect(
        **settings
    )
    connection.autocommit = True
    cursor = connection.cursor()

    try:
        cursor.execute(CREATE_USERS_TABLE)
        print("Users table created successfully")
    except DuplicateTable as e:
        print(f"Table already exists: {e}")

    cursor.close()
    connection.close()
except OperationalError as e:
    print(f"Error: {e}")

# connection to server and creating message table with error handling
try:
    connection = connect(
        **settings
    )
    connection.autocommit = True
    cursor = connection.cursor()

    try:
        cursor.execute(CREATE_MESSAGES_TABLE)
        print("Messages table created successfully")
    except DuplicateTable as e:
        print(f"Table already exists: {e}")

    cursor.close()
    connection.close()
except OperationalError as e:
    print(f"Error: {e}")

