import csv
import sqlite3
from abc import ABC, abstractmethod

class Expense:
    def __init__(self, date, category, name, amount):
        self.date = date
        self.category = category
        self.name = name
        self.amount = amount

    def display(self):
        print(self.date, "-", self.name, "-", self.category, "-", self.amount)

class StorageInterface(ABC):
    @abstractmethod
    def save(self, expenses):
        pass

    @abstractmethod
    def load(self):
        pass

class CSVStorage(StorageInterface):
    def __init__(self, filename="expenses.csv"):
        self.filename = filename

    def save(self, expenses):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "category", "name", "amount"])
            for expense in expenses:
                writer.writerow([
                    expense.date,
                    expense.category,
                    expense.name,
                    expense.amount
                ])

    def load(self):
        expenses = []
        try:
            with open(self.filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expense = Expense(
                        row["date"],
                        row["category"],
                        row["name"],
                        float(row["amount"])
                    )
                    expenses.append(expense)
        except FileNotFoundError:
            pass
        return expenses

class SQLiteStorage(StorageInterface):
    def __init__(self, database="expenses.db"):
        self.database = database
        self.create_table()

    def create_table(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                name TEXT,
                amount REAL
            )
        """)
        connection.commit()
        connection.close()

    def save(self, expenses):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM expenses")

        for expense in expenses:
            cursor.execute("""
                INSERT INTO expenses(date, category, name, amount)
                VALUES (?, ?, ?, ?)
            """, (
                expense.date,
                expense.category,
                expense.name,
                expense.amount
            ))

        connection.commit()
        connection.close()

    def load(self):
        expenses = []
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("SELECT date, category, name, amount FROM expenses")
        rows = cursor.fetchall()

        for row in rows:
            expense = Expense(
                row[0],
                row[1],
                row[2],
                row[3]
            )
            expenses.append(expense)

        connection.close()
        return expenses

class ExpenseManager:
    def __init__(self, storage):
        self.expenses = []
        self.storage = storage
        self.expenses = self.storage.load()

    def get_input(self):
        n = int(input("How many expenses do you want to enter? "))

        for i in range(n):
            print(f"\nEnter details for expense {i + 1}:")
            date = input("Enter Date (dd/mm/yyyy): ")
            category = input("Enter Category: ")
            name = input("Enter Name: ")
            amount = float(input("Enter Amount: "))

            expense = Expense(date, category, name, amount)
            self.expenses.append(expense)
            print("Expense added successfully!")

        self.storage.save(self.expenses)

    def show_expenses(self):
        if len(self.expenses) == 0:
            print("\nNo expenses found.")
            return

        print("\nExpenses:")
        for e in self.expenses:
            e.display()

    def total_spending(self):
        total = 0
        for e in self.expenses:
            total += e.amount
        return total

    def category_wise_spending(self):
        category_total = {}

        for e in self.expenses:
            if e.category in category_total:
                category_total[e.category] += e.amount
            else:
                category_total[e.category] = e.amount

        return category_total

    def show_summary(self):
        print("\nTotal Spending:", self.total_spending())
        print("\nCategory-wise Spending:")

        for category, amount in self.category_wise_spending().items():
            print(category, ":", amount)

    def update_expense(self):
        search_date = input("Enter Date (dd/mm/yyyy): ")
        matched_expenses = []

        for expense in self.expenses:
            if expense.date == search_date:
                matched_expenses.append(expense)

        if len(matched_expenses) == 0:
            print("\nNo expenses found on this date.")
            return

        print("\nExpenses on", search_date)

        for i in range(len(matched_expenses)):
            print(i + 1, end=". ")
            matched_expenses[i].display()

        choice = int(input("\nEnter the expense number to update: "))

        if choice < 1 or choice > len(matched_expenses):
            print("Invalid choice!")
            return

        expense = matched_expenses[choice - 1]

        print("\nEnter New Details")
        expense.category = input("Update New Category: ")
        expense.name = input("Update New Name: ")
        expense.amount = float(input("Update New Amount: "))

        print("\nExpense Updated Successfully!")
        self.storage.save(self.expenses)

    def delete_expense(self):
        search_date = input("Enter Date (dd/mm/yyyy): ")
        matched_expenses = []

        for expense in self.expenses:
            if expense.date == search_date:
                matched_expenses.append(expense)

        if len(matched_expenses) == 0:
            print("\nNo expenses found on this date.")
            return

        print("\nExpenses on", search_date)

        for i in range(len(matched_expenses)):
            print(i + 1, end=". ")
            matched_expenses[i].display()

        choice = int(input("\nEnter the expense number to delete: "))

        if choice < 1 or choice > len(matched_expenses):
            print("Invalid choice!")
            return

        expense = matched_expenses[choice - 1]
        self.expenses.remove(expense)

        print("\nExpense deleted successfully!")
        self.storage.save(self.expenses)

def main():
    print("------- EXPENSE MANAGER -------")
    print("1. CSV File")
    print("2. SQLite Database")

    storage_choice = input("Choose storage (1-2): ")

    if storage_choice == "1":
        storage = CSVStorage()
        print("CSV storage selected.")

    elif storage_choice == "2":
        storage = SQLiteStorage()
        print("SQLite storage selected.")

    else:
        print("Invalid choice!")
        return

    manager = ExpenseManager(storage)

    while True:
        print("\n------- Expense Manager -------")
        print("1. Add Expenses")
        print("2. Show Expenses")
        print("3. Show Summary")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            manager.get_input()

        elif choice == "2":
            manager.show_expenses()

        elif choice == "3":
            manager.show_summary()

        elif choice == "4":
            manager.update_expense()

        elif choice == "5":
            manager.delete_expense()

        elif choice == "6":
            print("Thank you for using the Expense Manager")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()