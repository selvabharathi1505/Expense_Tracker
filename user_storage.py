
import psycopg
from postgresql_storage import PostgreSQLStorage


class UserStorage:
    def __init__(self, connection_string=None):
        self.database = PostgreSQLStorage(connection_string)

    def create_user(self, username, email, password_hash):
        with self.database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING id, username, email, created_at
                    """,
                    (username, email, password_hash),
                )
                row = cursor.fetchone()

        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "created_at": row[3],
        }

    def username_or_email_exists(self, username, email):
        with self.database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1 FROM users
                    WHERE username = %s OR email = %s
                    LIMIT 1
                    """,
                    (username, email),
                )
                return cursor.fetchone() is not None

    def get_user_by_username(self, username):
        with self.database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, username, email, password_hash
                    FROM users
                    WHERE username = %s
                    """,
                    (username,),
                )
                row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
        }