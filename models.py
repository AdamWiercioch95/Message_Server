from psycopg2 import connect


class User:
    def __init__(self, username="", password=""):
        self._user_id = -1
        self.username = username
        self._password = password

    @property
    def user_id(self):
        return self._user_id

    @property
    def password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def save_to_db(self, crs):
        if self._user_id == -1:
            query = f"""
                INSERT INTO users (username, password) VALUES (
                '{self.username}', '{self.password}'
                )
                RETURNING id
            """
            crs.execute(query)
            self._user_id = crs.fetchone()[0]
        else:
            query = f"""
                UPDATE users SET 
                username = '{self.username}',
                password = '{self.password}'
                WHERE id = {self._user_id};
            """
            crs.execute(query)

    @staticmethod
    def load_user_by_username(crs, username):
        query = f"""
            SELECT id, username, password FROM users WHERE username = '{username}'
        """
        crs.execute(query)
        data = crs.fetchone()
        if data:
            id_, username, password = data
            loaded_user = User(username)
            loaded_user._user_id = id_
            loaded_user._password = password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_id(crs, user_id):
        query = f"""
            SELECT id, username, password FROM users WHERE id={user_id}
            """
        crs.execute(query)
        data = crs.fetchone()
        if data:
            id_, username, password = data
            loaded_user = User(username)
            loaded_user._user_id = id_
            loaded_user._password = password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(crs):
        query = f"""
            SELECT * FROM users
        """
        users = []
        crs.execute(query)
        for row in crs.fetchall():
            id_, username, password = row
            loaded_user = User()
            loaded_user._user_id = id_
            loaded_user._password = password
            loaded_user.username = username
            users.append(loaded_user)
        return users

    def delete(self, crs):
        query = f"""
            DELETE FROM users WHERE id={self._user_id}
        """
        crs.execute(query)
        self._user_id = -1
        return True


class Message:
    def __init__(self, from_user_id, to_user_id, text):
        self._id = -1
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.text = text
        self._creation_date = None

    @property
    def id(self):
        return self._id

    @property
    def creation_date(self):
        return self._creation_date

    def save_to_db(self, crs):
        if self._id == -1:
            query = f"""
                INSERT INTO messages (from_id, to_user_id, text) VALUES (
                    {self.from_user_id}, {self.to_user_id}, '{self.content}'
                );
                RETURNING id, creation_date;
            """
            crs.execute(query)
            self._id, self_creation_date = crs.fetchone()
        # poprawić create_db.py -> nazwy column w tabeli
        else:
            query = f"""
                UPDATE messages SET 
                    from_id={self.from_user_id}, 
                    to_user_id={self.to_user_id}, 
                    text='{self.text}'
                    WHERE id = {self._id};
            """
            crs.execute(query)

    @staticmethod
    def load_all_messages(crs, id_=None):
        if id_ is None:
            query = f"""
                SELECT * FROM messages
            """
        else:
            query = f"""
                SELECT * FROM messages WHERE id={id_};
            """
        messages = []
        crs.execute(query)
        for row in crs.fetchall():
            id_, from_id, to_user_id, text, creation_date = row
            loaded_message = Message(from_id, to_user_id, text)
            loaded_message._self_id = id_
            loaded_message._creation_date = creation_date
            messages.append(loaded_message)
        return messages


# settings = {
#     'host': 'localhost',
#     'database': 'message_server_db',
#     'user': 'postgres',
#     'password': 'coderslab',
#     'port': 5432
# }
# connection = connect(**settings)
# cursor = connection.cursor()
#
# result1 = User.load_user_by_id(cursor, 4)
# print(result1._user_id, result1._password, result1.username)
#
# result2 = User.load_all_users(cursor)
# print("wyświetlam wszystkich")
# for user in result2:
#     print(user.user_id, user.username, user.password)
#
# print("Usuwam")
# result1.delete(cursor)
# connection.commit()
#
# result2 = User.load_all_users(cursor)
# print("wyświetlam wszystkich")
# for user in result2:
#     print(user.user_id, user.username, user.password)
#
# connection.commit()
# cursor.close()
# connection.close()
