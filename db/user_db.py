import pyodbc


class UserDatabase:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=AryantNigam;DATABASE=restaurent;')
    cursor = conn.cursor()

    @classmethod
    def get_users(cls):
        response = []
        query = f"SELECT id, username FROM users"

        users_data = cls.cursor.execute(query).fetchall()
        for user in users_data:
            response.append(
                {
                   'id': user[0],
                   'username': user[1]
                }
            )
        return response

    @classmethod
    def get_user(cls, user_id):
        query = f"SELECT id, username, password FROM users WHERE id = {user_id}"
        user_data = cls.cursor.execute(query).fetchone()
        user = {
               'id': user_data[0],
               'username': user_data[1],
        }
        return user

    @classmethod
    def add_user(cls, username, password):
        try:
            query = f"INSERT INTO users (username, password) VALUES ('{username}','{password}')"
            cls.cursor.execute(query)
            cls.conn.commit()
            return True
        except pyodbc.IntegrityError:
            return False


    @classmethod
    def delete_user(cls, user_id):
        query = f"DELETE FROM users WHERE id = {user_id}"
        affected_rows = cls.cursor.execute(query).rowcount
        cls.conn.commit()
        return affected_rows

    @classmethod
    def verify_user(cls, username, hashed_password):
        query = f"SELECT * FROM users WHERE username='{username}'"
        response = cls.cursor.execute(query).fetchone()
        if response:
            # user exists
            saved_password = response[2]
            if saved_password == hashed_password:
                # password is correct generate JWT token
                return {"code": 200, "identity": {'id': response[0], 'username': username}}
            else:
                # password is incorrect
                return {"code": 401, "message": "Invalid password"}
        else:
            # user does not exist
            return {"code": 401, "message": "Invalid username"}

