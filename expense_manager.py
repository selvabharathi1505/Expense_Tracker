from expense import Expense

class ExpenseManager:

    def __init__(self, storage):
        self.storage = storage

    def get_next_id(self):
        expenses = self.storage.load()

        if not expenses:
            return 1

        return max(e.id for e in expenses) + 1
    
    def get_expenses(self):
        return self.storage.load()


    def get_expense(self, expense_id):
        expenses = self.storage.load()

        for expense in expenses:
            if expense.id == expense_id:
                return expense

        return None

    def add_expense(self, name, category, amount, date):
        expense_id = self.get_next_id()
        expense = Expense(expense_id, name, category, amount, date)

        self.storage.add(expense)
        
        return expense


    def show_expenses(self):
        expenses = self.storage.load()

        if not expenses:
            print("No expenses found.")
            return

        for expense in expenses:
            expense.display()

    def update_expense(self, expense_id, name, category, amount, date):
        expenses = self.storage.load()

        found = False

        for expense in expenses:
            if expense.id == expense_id:
                found = True
                break

        if not found:
            return False

        expense = Expense(expense_id, name, category, amount, date)
        self.storage.update(expense_id, expense)

        return True

    def delete_expense(self, expense_id):
        
        expenses = self.storage.load()
       

        found = False
        
        for expense in expenses:
            if expense.id == expense_id:
                found = True
                break

        if not found:
            
            return False
    
        self.storage.delete(expense_id)

        
        return True
    
    def total_spending(self):
        expenses = self.storage.load()

        if len(expenses) == 0:
            return 0

        total = 0
        for expense in expenses:
            total += expense.amount

        return total


    def category_wise_spending(self):
        expenses = self.storage.load()

        category_totals = {}

        for expense in expenses:
            if expense.category in category_totals:
                category_totals[expense.category] += expense.amount
            else:
                category_totals[expense.category] = expense.amount

        return category_totals
        
    def show_summary(self):

        print("\nExpense Summary:")
        print(f"Total Spending: $ {self.total_spending()}")

        print("\nCategory-wise Spending:")
        
        category_totals = self.category_wise_spending()
        
        if len(category_totals) == 0:
            print("No expenses found.")
            return
        
        for category, total in category_totals.items():
            print(f"{category}: $ {total:.2f}")
            
   

        