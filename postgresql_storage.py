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
        cursor.fetchall()
        