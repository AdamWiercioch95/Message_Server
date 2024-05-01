from crypto import hash_password


class User:
    def __init__(self, username="", password="", salt=""):
        self._user_id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def user_id(self):
        return self._user_id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, crs):
        if self._user_id == -1:
            query = """
                INSERT INTO users (username, password) VALUES (%s, %s)
                RETURNING id
            """
            crs.execute(query, (self.username, self.hashed_password))
            self._user_id = crs.fetchone()[0]
            return True
        else:
            query = f"""
                UPDATE users 
                SET username = %s, password = %s
                WHERE id = %s;
            """
            crs.execute(query, (self.username, self.hashed_password, self._user_id))
            return True

    @staticmethod
    def load_user_by_username(crs, username):
        query = f"""
            SELECT id, username, password FROM users WHERE username = %s
        """
        crs.execute(query, (username,))
        data = crs.fetchone()
        if data:
            id_, username, password = data
            loaded_user = User(username)
            loaded_user._user_id = id_
            loaded_user._hashed_password = password
            return loaded_user

    @staticmethod
    def load_user_by_id(crs, user_id):
        query = f"""
            SELECT id, username, password FROM users WHERE id=%s
            """
        crs.execute(query, (user_id,))
        data = crs.fetchone()
        if data:
            id_, username, password = data
            loaded_user = User(username)
            loaded_user._user_id = id_
            loaded_user._hashed_password = password
            return loaded_user

    @staticmethod
    def load_all_users(crs):
        query = f"""
            SELECT id, username, password FROM users
        """
        users = []
        crs.execute(query)
        for row in crs.fetchall():
            id_, username, password = row
            loaded_user = User()
            loaded_user._user_id = id_
            loaded_user._hashed_password = password
            loaded_user.username = username
            users.append(loaded_user)
        return users

    def delete(self, crs):
        query = f"""
            DELETE FROM users WHERE id=%s
        """
        crs.execute(query, (self._user_id,))
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
                INSERT INTO messages (from_id, to_user_id, text) VALUES (%s, %s, %s);
                RETURNING id, creation_date;
            """
            crs.execute(query, (self.from_user_id, self.to_user_id, self.text))
            self._id, self_creation_date = crs.fetchone()
            return True
        # poprawić create_db.py -> nazwy column w tabeli
        else:
            query = f"""
                UPDATE messages SET 
                    from_id=%s, 
                    to_user_id=%s, 
                    text=%s
                    WHERE id=%s;
            """
            crs.execute(query, (self.from_user_id, self.to_user_id, self.text, self._id))
            return True

    @staticmethod
    def load_all_messages(crs, id_=None):
        if id_ is None:
            query = f"""
                SELECT id, from_id, to_id, text, creation_date FROM messages
            """
            crs.execute(query)
        else:
            query = f"""
                SELECT id, from_id, to_id, text, creation_date FROM messages WHERE id=%s;
            """
            crs.execute(query, (id_,))

        messages = []
        for row in crs.fetchall():
            id_, from_id, to_user_id, text, creation_date = row
            loaded_message = Message(from_id, to_user_id, text)
            loaded_message._self_id = id_
            loaded_message._creation_date = creation_date
            messages.append(loaded_message)
        return messages
