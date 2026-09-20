import psycopg
from expense import Expense

class PostgresSQLStorage:
    def __init__ (self, connection_string):
        self.connection_string = connection_string
    
    def get_connection(self):
        return psycopg.connect(self.connection_string)
    def load(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category, amount, date FROM expenses")
        rows=cursor.fetchall()
        expenses = []
        for row in rows:
            expense = Expense(row[0], row[1], row[2], float(row[3]), row[4])
            expenses.append(expense)
        cursor.close()
        conn.close()
        return expenses
        
storage = PostgresSQLStorage("dbname=expense_tracker user=postgres password=selva host=localhost")

expenses = storage.load()

for expense in expenses:
    expense.display()