class User:
    def __init__(self, user_id, username, password):
        self._user_id = user_id
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