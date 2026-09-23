from expense import Expense

class ExpenseManager:

    def __init__(self, storage):
        self.storage = storage

    def get_expenses(self, limit=20, offset=0):
        return self.storage.get_expenses(limit, offset)

    def get_expense(self, expense_id):
        return self.storage.get_by_id(expense_id)

    def add_expense(self, name, category, amount, expense_date):
        expense = Expense(None, name, category, amount, expense_date)

        return self.storage.add(expense)

    def show_expenses(self, limit=20, offset=0):
        expenses = self.get_expenses(limit, offset)

        if not expenses:
            print("No expenses found.")
            return

        for expense in expenses:
            expense.display()

    def update_expense(self, expense_id, name, category, amount, expense_date):
        expense = Expense(expense_id, name, category, amount, expense_date)
        return self.storage.update(expense_id, expense)

    def delete_expense(self, expense_id):
        return self.storage.delete(expense_id)

    def total_spending(self):
        return self.storage.total_spending()

    def category_wise_spending(self):
        return self.storage.category_wise_spending()

    def show_summary(self):
        print("\nExpense Summary:")
        print(f"Total Spending: $ {self.total_spending():.2f}")

        print("\nCategory-wise Spending:")

        category_totals = self.category_wise_spending()

        if not category_totals:
            print("No expenses found.")
            return

        for category, total in category_totals.items():
            print(f"{category}: $ {total:.2f}")