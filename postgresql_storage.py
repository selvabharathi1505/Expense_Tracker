import psycopg
from expense import Expense
from storage import Storage
import os
from dotenv import load_dotenv
load_dotenv()

class PostgreSQLStorage(Storage):
    def __init__(self, connection_string=None):
        self.connection_string = connection_string or os.getenv("DATABASE_URL")
    
    def get_connection(self):
        return psycopg.connect(self.connection_string)
    
    def get_expenses(self, limit=20, offset=0):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, category, amount, date FROM expenses
            ORDER BY id
            LIMIT %s OFFSET %s
            """,
            (limit, offset))

        rows = cursor.fetchall()

        expenses = []
        for row in rows:
            expense = Expense(row[0], row[1], row[2], float(row[3]), row[4])
            expenses.append(expense)

        cursor.close()
        conn.close()

        return expenses
    
    def get_by_id(self, expense_id):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, category, amount, date FROM expenses
            WHERE id = %s
            """,(expense_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:
            return None

        return Expense(row[0],row[1],row[2],float(row[3]),row[4])

    def add(self, expense):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO expenses (name, category, amount, date)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,(expense.name, expense.category, expense.amount, expense.date))
        
        expense_id = cursor.fetchone()[0]
        
        conn.commit()
        cursor.close()
        conn.close()
        return Expense(expense_id, expense.name, expense.category, expense.amount, expense.date)
    
    def update(self, expense_id, expense):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE expenses
            SET name = %s, category = %s, amount = %s, date = %s
            WHERE id = %s
            """,(expense.name, expense.category, expense.amount, expense.date, expense_id))
        updated = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return updated
    
    def delete(self, expense_id):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM expenses
            WHERE id = %s
            """,(expense_id,))

        deleted = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()

        return deleted

    def total_spending(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            """)

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return float(total or 0)
    
    def category_wise_spending(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
            """
        )

        rows = cursor.fetchall()

        category_totals = {}

        for row in rows:
            category_totals[row[0]] = float(row[1])

        cursor.close()
        conn.close()

        return category_totals