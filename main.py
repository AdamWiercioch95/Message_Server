from psycopg2 import connect
from psycopg2.errors import UniqueViolation
from create_db import create_db
from models import User, Message


interface = """
Welcome to Message Server!
--------------------------
What would you like to do?

1. Create Database
2. List All Users
3. Search User By Id
4. Search User By Username
5. Add User
6. Modify User
7. Delete User
8. Create Message
9. Modify Message
10. Load All Messages
11. Load Message By Id
12. Exit
"""

settings = {
    'host': 'localhost',
    'database': 'message_server_db',
    'user': 'postgres',
    'password': 'coderslab',
    'port': 5432
}

while True:
    choice = input(interface)
    connection = connect(**settings)
    cursor = connection.cursor()

    # jak dodać bezpośrednie wywołanie skryptu?
    if choice == "1":
        create_db()

    elif choice == "2":
        users = User.load_all_users(cursor)
        for user in users:
            print(f"""Id: {user.user_id}, Username: {user.username}, Password: {user.password}""")
        cursor.close()
        connection.close()

    elif choice == "3":
        user_id = input("Enter User ID: ")
        user = User.load_user_by_id(cursor, user_id)
        # czy jest wyjątek do sprawdzenia, czy id istnieje w bazie danych?
        if user:
            print(f"""Id: {user.user_id}, Username: {user.username}, Password: {user.password}""")
        else:
            print("User not found")
        cursor.close()
        connection.close()

    elif choice == "4":
        username = input("Enter Username: ")
        user = User.load_user_by_username(cursor, username)
        if user:
            print(f"""Id: {user.user_id}, Username: {user.username}, Password: {user.password}""")
        else:
            print("User not found")
        cursor.close()
        connection.close()

    elif choice == "5":
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        try:
            user = User(username, password)
            user.save_to_db(cursor)
            print("User added to database")
        except UniqueViolation:
            print("User with given data already exists")
        connection.commit()
        cursor.close()
        connection.close()

    # Dlaczego po modyfikacji, w konsoli wyświetla się lista w innej kolejności niż w bazie danych?
    elif choice == "6":
        id_ = input("Enter User ID: ")
        user = User.load_user_by_id(cursor, id_)
        if user:
            username = input("Enter new Username: ")
            password = input("Enter new Password: ")
            user.username = username
            user.set_password(password)
            user.save_to_db(cursor)
            connection.commit()
        else:
            print("User not found")
        cursor.close()
        connection.close()

    elif choice == "7":
        id_ = input("Enter User ID: ")
        user = User.load_user_by_id(cursor, id_)
        if user:
            user.delete(cursor)
            connection.commit()
            print("User deleted")
        else:
            print("User not found")
        cursor.close()
        connection.close()

    elif choice == "8":
        pass
    elif choice == "9":
        pass
    elif choice == "10":
        pass
    elif choice == "11":
        pass
    elif choice == "12":
        break
