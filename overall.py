import csv
import sqlite3
import argparse
class Expense:

    def __init__(self, id, name, category, amount, date):
        self.id = id
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date

    def display(self):
        print(self.id, "-", self.date, "-", self.name, "-", self.category, "-", self.amount)

from abc import ABC, abstractmethod
class Storage(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def add(self, expense):
        pass

    @abstractmethod
    def update(self, expense_id, expense):
        pass

    @abstractmethod
    def delete(self, expense_id):
        pass


class CSVStorage(Storage):

    def __init__(self, filename="expenses.csv"):
        self.filename = filename

    def load(self):
        expenses = []

        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    expense = Expense(int(row["id"]), row["name"], row["category"], float(row["amount"]), row["date"])
                    expenses.append(expense)

        except FileNotFoundError:
            pass

        return expenses

    def add(self, expense):
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(["id", "name", "category", "amount", "date"])

            writer.writerow([expense.id, expense.name, expense.category, expense.amount, expense.date])

    def update(self, expense_id, expense):
        expenses = self.load()

        for e in expenses:
            if e.id == expense_id:
                e.name = expense.name
                e.category = expense.category
                e.amount = expense.amount
                e.date = expense.date

        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "category", "amount", "date"])

            for e in expenses:
                writer.writerow([e.id, e.name, e.category, e.amount, e.date])

    def delete(self, expense_id):
        expenses = self.load()
        expenses = [e for e in expenses if e.id != expense_id]

        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "category", "amount", "date"])

            for e in expenses:
                writer.writerow([e.id, e.name, e.category, e.amount, e.date])



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
                expenses.append(Expense(row[0], row[1], row[2], row[3], row[4]))

        return expenses

    def add(self, expense):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("""
                INSERT INTO expenses (id, name, category, amount, date)
                VALUES (?, ?, ?, ?, ?)
            """, (expense.id, expense.name, expense.category, expense.amount, expense.date))

    def update(self, expense_id, expense):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("""
                UPDATE expenses
                SET name = ?, category = ?, amount = ?, date = ?
                WHERE id = ?
            """, (expense.name, expense.category, expense.amount, expense.date, expense_id))

    def delete(self, expense_id):
        with sqlite3.connect(self.filename) as conn:
            conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

from expense import Expense



class ExpenseManager:

    def __init__(self, storage):
        self.storage = storage

    def get_next_id(self):
        expenses = self.storage.load()

        if not expenses:
            return 1

        max_id = 0
        for expense in expenses:
            if expense.id > max_id:
                max_id = expense.id

        return max_id + 1

    def add_expense(self):
        choice= int(input("enter how many expenses to be added: "))
        for i in range(choice):
            
            expense_id = self.get_next_id()
            print(f"Enter the details for expense {i+1}: ")
            name = input("Enter Name: ")
            category = input("Enter Category: ")
            amount = float(input("Enter Amount: "))
            date = input("Enter Date (dd/mm/yyyy): ")

            expense = Expense(expense_id, name, category, amount, date)
            self.storage.add(expense)

        print("Expense added successfully.")

    def show_expenses(self):
        expenses = self.storage.load()

        if not expenses:
            print("No expenses found.")
            return

        for expense in expenses:
            expense.display()

    def update_expense(self):
        self.show_expenses()
        expenses = self.storage.load()
        if len(expenses) == 0:
            return
        
        expense_id = int(input("Enter ID to update: "))
        found = False
        
        for expense in expenses:
            if expense.id == expense_id:
                found = True
                break

        if not found:
            print("Expense ID not found")
            return
        
        name = input("Enter new Name: ")
        category = input("Enter new Category: ")
        amount = float(input("Enter new Amount: "))
        date = input("Enter new Date: ")

        expense = Expense(expense_id, name, category, amount, date)
        self.storage.update(expense_id, expense)

        print("Expense updated successfully.")

    def delete_expense(self):
        self.show_expenses()
        
        expenses = self.storage.load()
        if len(expenses) == 0:
            return

        expense_id = int(input("Enter ID to delete: "))
        found = False
        
        for expense in expenses:
            if expense.id == expense_id:
                found = True
                break

        if not found:
            print("Expense ID not found")
            return
    
        self.storage.delete(expense_id)

        print("Expense deleted successfully.")




def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--storage",
        choices=["csv", "sqlite"],
        required=True,
        help="Choose storage type: csv or sqlite"
    )

    args = parser.parse_args()

    if args.storage == "csv":
        print("Using CSV Storage")
        storage = CSVStorage()

    elif args.storage == "sqlite":
        print("Using SQLite Storage")
        storage = SQLiteStorage()

    manager = ExpenseManager(storage)

    while True:

        print("\n1. Add Expense")
        print("2. Show Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            manager.add_expense()

        elif choice == "2":
            manager.show_expenses()

        elif choice == "3":
            manager.update_expense()

        elif choice == "4":
            manager.delete_expense()

        elif choice == "5":
            print("Program ended.")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()