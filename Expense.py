class Expense:
    def __init__(self, name, category, amount, date):
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date

    def display(self):
        print(self.date, "-", self.name, "-", self.category, "-", self.amount)


class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def get_input(self):
        n = int(input("How many expenses do you want to enter? "))
        for i in range(n):
            print(f"\nEnter details for expense {i + 1}:")
            name = input("Enter Name: ")
            category = input("Enter Category: ")
            amount = float(input("Enter Amount: "))
            date = input("Enter Date (dd/mm/yyyy): ")
            expense = Expense(name, category, amount, date)
            self.expenses.append(expense)

    def show_expenses(self):
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

        search_date = input("Enter the date of the expense to update (dd/mm/yyyy): ")

        found = False

        for expense in self.expenses:

            if expense.date == search_date:

                print("\nExpense Found:")
                expense.display()

                expense.name = input("Enter new name: ")
                expense.category = input("Enter new category: ")
                expense.amount = float(input("Enter new amount: "))

                print("\nExpense Updated Successfully!")
                found = True
                break

        if not found:
            print("No expense found on this date.")
                
        

    
    
def main():
    manager = ExpenseManager()
    manager.get_input()
    manager.show_expenses()
    manager.show_summary()
    manager.update_expense()
         
if __name__ == "__main__":
    main()
    