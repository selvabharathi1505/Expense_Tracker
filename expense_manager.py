from expense import Expense



class ExpenseManager:

    def __init__(self, storage):
        self.storage = storage

    def get_next_id(self):
        expenses = self.storage.load()

        if not expenses:
            return 1

        return max(e.id for e in expenses) + 1

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
