import csv
from expense import Expense
from storage import Storage
from datetime import datetime

class CSVStorage(Storage):

    def __init__(self, filename="expenses.csv"):
        self.filename = filename

    def load(self):
        expenses = []

        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    expenses.append(Expense(int(row["id"]), row["name"], row["category"], float(row["amount"]), datetime.strptime(row["date"], "%d/%m/%Y").date()))

        except FileNotFoundError:
            pass

        return expenses

    def add(self, expense):
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(["id", "name", "category", "amount", "date"])

            writer.writerow([expense.id, expense.name, expense.category, expense.amount, expense.date.strftime("%d/%m/%Y")])

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
                writer.writerow([e.id, e.name, e.category, e.amount, e.date.strftime("%d/%m/%Y")])

    def delete(self, expense_id):
        expenses = self.load()
        expenses = [e for e in expenses if e.id != expense_id]

        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "category", "amount", "date"])

            for e in expenses:
                writer.writerow([e.id, e.name, e.category, e.amount, e.date.strftime("%d/%m/%Y")])

