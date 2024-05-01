import argparse

import psycopg2
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

from crypto import check_password, hash_password
from models import User

# parser.add_argument("-u",
#                     "--username",
#                     help="""python3 <filename> -u <username>
#                             python3 <filename> -username <username>""")
#
# parser.add_argument("-p",
#                     "--password",
#                     help="""python3 <filename> -p <password>
#                             python3 <filename> -password <password>
#                              (password mus have at least 8 characters)""")

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (at least 8 characters)")
parser.add_argument("-n", "--new_pass", help="enter new password (at least 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
args = parser.parse_args()


def create_user(crs, username, password):
    if len(password) < 8:
        print("Password must be at least 8 characters")
    else:
        try:
            user = User(username, password)
            user.save_to_db(crs)
            print("User created successfully")
        except UniqueViolation as e:
            print("User already exists. ", e)


def edit_user(crs, username, password, new_password):
    user = User.load_user_by_username(crs, username)
    if user is None:
        print("User not found")

    if len(password) < 8:
        print("Password must be at least 8 characters")
    elif check_password(password, user.hashed_password):
        if len(new_password) < 8:
            print("New password must be at least 8 characters")
        else:
            user.hashed_password = new_password
            user.save_to_db(crs)
            print("Password updated successfully")
    else:
        print("Password is incorrect")


def delete_user(crs, username, password):
    user = User.load_user_by_username(crs, username)
    if user is None:
        print("User not found")

    if len(password) < 8:
        print("Password must be at least 8 characters")
    elif check_password(password, user.hashed_password):
        user.delete(crs)
        print("User deleted successfully")
    else:
        print("Password is incorrect")


def list_users(crs):
    users = User.load_all_users(crs)
    for user in users:
        print(user.username)


if __name__ == "__main__":
    try:
        connection = connect(
            host="localhost",
            port=5432,
            database="message_server_db",
            user="postgres",
            password="coderslab"
        )
        connection.autocommit = True
        cursor = connection.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()
        cursor.close()
        connection.close()
    except OperationalError as e:
        print("Connection error: ", e)
