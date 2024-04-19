from psycopg2 import connect
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


while True:
    choice = input(interface)
    if choice == "1":
        create_db()
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        pass
    elif choice == "6":
        pass
    elif choice == "7":
        pass
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
