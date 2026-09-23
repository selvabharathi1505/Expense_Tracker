from datetime import date
class Expense:

    def __init__(self, id, name, category, amount, expense_date: date):
        self.id = id
        self.name = name
        self.category = category
        self.amount = amount
        self.date = expense_date

    def display(self):
        print(self.id, "-", self.date, "-", self.name, "-", self.category, "-", self.amount)









