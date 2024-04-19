from psycopg2 import connect


class User:
    def __init__(self, username, password):
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
            return True
        return False


settings = {
    'host': 'localhost',
    'database': 'message_server_db',
    'user': 'postgres',
    'password': 'coderslab',
    'port': 5432
}
connection = connect(**settings)
cursor = connection.cursor()

u2 = User('user2', 'password2')
u2.save_to_db(cursor)
connection.commit()
cursor.close()
connection.close()

# u.set_password('dupa')
# print(u.user_id)
# print(u.username)
# print(u.password)
