
from expense import Expense


class ExpenseManager:

    def __init__(self, storage):
        self.storage = storage

    def get_expenses(self, user_id, limit=20, offset=0):
        return self.storage.get_expenses(user_id, limit, offset)

    def get_expense(self, expense_id, user_id):
        return self.storage.get_by_id(expense_id, user_id)

    def add_expense(self, name, category, amount, expense_date, user_id):
        expense = Expense(None, name, category, amount, expense_date)
        return self.storage.add(expense, user_id)

    def update_expense(
        self, expense_id, name, category, amount, expense_date, user_id
    ):
        expense = Expense(expense_id, name, category, amount, expense_date)
        return self.storage.update(expense_id, expense, user_id)

    def delete_expense(self, expense_id, user_id):
        return self.storage.delete(expense_id, user_id)

    def total_spending(self, user_id):
        return self.storage.total_spending(user_id)

    def category_wise_spending(self, user_id):
        return self.storage.category_wise_spending(user_id)
