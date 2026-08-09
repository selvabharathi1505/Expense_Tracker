import csv
class Expense:
    def __init__(self, date, category, name , amount):
        self.date = date
        self.category = category
        self.name = name
        self.amount = amount

    def display(self):
        print(self.date, "-", self.name, "-", self.category, "-", self.amount)

class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def get_input(self):
        n = int(input("How many expenses do you want to enter? "))
        for i in range(n):
            print(f"\nEnter details for expense {i + 1}: ")
            date = input("Enter Date (dd/mm/yyyy): ")
            category = input("Enter Category: ")
            name = input("Enter Name: ")
            amount = float(input("Enter Amount: "))

            expense = Expense(date, category, name, amount )
            self.expenses.append(expense)
            print("Expense added successfully!")
            self.save_to_csv()

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

        search_date = input("Enter Date (dd/mm/yyyy): ")

        matched_expenses = []

        # Find all expenses on the entered date
        for expense in self.expenses:
            if expense.date == search_date:
                matched_expenses.append(expense)

        # If no expense found
        if len(matched_expenses) == 0:
            print("\nNo expenses found on this date.")
            return

        # Display all matching expenses
        print("\nExpenses on", search_date)
        for i in range(len(matched_expenses)):
            print(i + 1, end=". ")
            matched_expenses[i].display()

        # Select which expense to update
        choice = int(input("\nEnter the expense number to update: "))

        if choice < 1 or choice > len(matched_expenses):
            print("Invalid choice!")
            return

        # Selected expense
        expense = matched_expenses[choice - 1]

        print("\nEnter New Details")

        expense.category = input("Enter New Category: ")
        expense.name = input("Enter New Name: ")
        expense.amount = float(input("Enter New Amount: "))

        print("\nExpense Updated Successfully!")
        self.save_to_csv()

    def save_to_csv(self):
        with open("expenses.csv", "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["date", "category", "name", "amount"])

            for expense in self.expenses:
                writer.writerow([
                    expense.date,
                    expense.category,
                    expense.name,
                    expense.amount
                ])

    def load_from_csv(self):
        try:
            with open("expenses.csv", "r") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    expense = Expense(
                        row["date"],
                        row["category"],
                        row["name"],
                        float(row["amount"])
                    )

                    self.expenses.append(expense)

        except FileNotFoundError:
            pass


def main():
    manager = ExpenseManager()
    manager.load_from_csv()

    while True:
        print("\n------- Expense Manager -------")
        print("Enter 1 for  Add Expenses")
        print("Enter 2 for  Show Expenses")
        print("Enter 3 for  Show Summary")
        print("Enter 4 for  Update Expense")
        print("Enter 5 for  Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            manager.get_input()

        elif choice == "2":
            manager.show_expenses()

        elif choice == "3":
            manager.show_summary()

        elif choice == "4":
            manager.update_expense()

        elif choice == "5":
            print("Thank you for using Expense Manager!")
            break

        else:
            print("Invalid choice. Please enter a valid option within (1-5).")


if __name__ == "__main__":
    main()