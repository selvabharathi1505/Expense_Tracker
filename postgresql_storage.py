
import os

import psycopg
from dotenv import load_dotenv

from expense import Expense
from storage import Storage

load_dotenv()


class PostgreSQLStorage(Storage):
    def __init__(self, connection_string=None):
        self.connection_string = (
            connection_string or os.getenv("DATABASE_URL")
        )

    def get_connection(self):
        if not self.connection_string:
            raise RuntimeError("DATABASE_URL is not configured.")
        return psycopg.connect(self.connection_string)

    def get_expenses(self, user_id, limit=20, offset=0):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, category, amount, date
                    FROM expenses
                    WHERE user_id = %s
                    ORDER BY id
                    LIMIT %s OFFSET %s
                    """,
                    (user_id, limit, offset),
                )
                rows = cursor.fetchall()

        return [
            Expense(
                row[0],
                row[1],
                row[2],
                float(row[3]),
                row[4],
            )
            for row in rows
        ]

    def get_by_id(self, expense_id, user_id):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, category, amount, date
                    FROM expenses
                    WHERE id = %s AND user_id = %s
                    """,
                    (expense_id, user_id),
                )
                row = cursor.fetchone()

        if row is None:
            return None

        return Expense(
            row[0],
            row[1],
            row[2],
            float(row[3]),
            row[4],
        )

    def add(self, expense, user_id):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO expenses
                        (name, category, amount, date, user_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        expense.name,
                        expense.category,
                        expense.amount,
                        expense.date,
                        user_id,
                    ),
                )
                expense_id = cursor.fetchone()[0]

        return Expense(
            expense_id,
            expense.name,
            expense.category,
            expense.amount,
            expense.date,
        )

    def update(self, expense_id, expense, user_id):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE expenses
                    SET name = %s,
                        category = %s,
                        amount = %s,
                        date = %s
                    WHERE id = %s AND user_id = %s
                    """,
                    (
                        expense.name,
                        expense.category,
                        expense.amount,
                        expense.date,
                        expense_id,
                        user_id,
                    ),
                )
                return cursor.rowcount > 0

    def delete(self, expense_id, user_id):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM expenses
                    WHERE id = %s AND user_id = %s
                    """,
                    (expense_id, user_id),
                )
                return cursor.rowcount > 0

    def total_spending(self, user_id):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COALESCE(SUM(amount), 0)
                    FROM expenses
                    WHERE user_id = %s
                    """,
                    (user_id,),
                )
                return float(cursor.fetchone()[0])

    def category_wise_spending(self, user_id):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT category, SUM(amount)
                    FROM expenses
                    WHERE user_id = %s
                    GROUP BY category
                    ORDER BY category
                    """,
                    (user_id,),
                )
                rows = cursor.fetchall()

        return {
            row[0]: float(row[1])
            for row in rows
        }
