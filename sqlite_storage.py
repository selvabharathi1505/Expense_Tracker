import sqlite3
from expense import Expense
from storage import Storage
from datetime import datetime

class SQLiteStorage(Storage):

    def __init__(self, filename="expenses.db"):
        self.filename = filename
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    category TEXT,
                    amount REAL,
                    date TEXT
                )
            """)

    def load(self):
        expenses = []

        with sqlite3.connect(self.filename) as conn:
            cursor = conn.execute("SELECT id, name, category, amount, date FROM expenses")

            for row in cursor:
                expenses.append(Expense(row[0], row[1], row[2], row[3], datetime.strptime(row[4], "%d/%m/%Y").date()))

        return expenses

    def add(self, expense):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("""
                INSERT INTO expenses (id, name, category, amount, date)
                VALUES (?, ?, ?, ?, ?)
            """, (expense.id, expense.name, expense.category, expense.amount, expense.date.strftime("%d/%m/%Y")))

    def update(self, expense_id, expense):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("""
                UPDATE expenses
                SET name = ?, category = ?, amount = ?, date = ?
                WHERE id = ?
            """, (expense.name, expense.category, expense.amount, expense.date.strftime("%d/%m/%Y"), expense_id))

    def delete(self, expense_id):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

