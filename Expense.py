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

    def add_expenses(self):
        n = int(input("How many expanses do you want to enter?¨"))

        for i in range(n):
            print("\nExpense", i + 1)

            name = input("Enter Name: ")
            category = input("Enter Category: ")
            amount = float(input("Enter Amount: "))
            date = input("Enter Date: ")

            expense = Expense(name, category, amount, date)
            self.expenses.append(expense)

    def display_expenses(self):
        print("\nExpense List")
        for expense in self.expenses:
            expense.display()

    def total_spending(self):
        total = 0
        for expense in self.expenses:
            total += expense.amount
        return total

    def category_spending(self):
        data = {}

        for expense in self.expenses:
            if expense.category in data:
                data[expense.category] += expense.amount
            else:
                data[expense.category] = expense.amount

        return data

    def summary(self):
        print("\nTotal Spending:", self.total_spending())

        print("\nCategory-wise Spending")
        data = self.category_spending()

        for category in data:
            print(category, ":", data[category])


def main():
    manager = ExpenseManager()
    manager.add_expenses()
    manager.display_expenses()
    manager.summary()


if __name__ == "__main__":
    main()