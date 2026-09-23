from datetime import datetime

from expense_manager import ExpenseManager
from postgresql_storage import PostgreSQLStorage


def main():

    storage = PostgreSQLStorage()
    manager = ExpenseManager(storage)

    while True:

        print("\n1. Add Expense")
        print("2. Show Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Show Summary")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            count = int(input("Enter how many expenses to be added: "))

            for i in range(count):

                print(f"Enter the details for expense {i + 1}:")

                name = input("Enter Name: ")
                category = input("Enter Category: ")
                amount = float(input("Enter Amount: "))

                expense_date = datetime.strptime(
                    input("Enter Date (yyyy-mm-dd): "),
                    "%Y-%m-%d"
                ).date()

                manager.add_expense(
                    name,
                    category,
                    amount,
                    expense_date
                )

            print("Expense added successfully.")

        elif choice == "2":
            manager.show_expenses()

        elif choice == "3":
            manager.show_expenses()

            expenses = manager.get_expenses()

            if not expenses:
                print("No expenses available to update.")
                continue

            expense_id = int(input("Enter ID to update: "))

            name = input("Enter new Name: ")
            category = input("Enter new Category: ")
            amount = float(input("Enter new Amount: "))

            expense_date = datetime.strptime(
                input("Enter new Date (yyyy-mm-dd): "),
                "%Y-%m-%d"
            ).date()

            result = manager.update_expense(
                expense_id,
                name,
                category,
                amount,
                expense_date
            )

            if result:
                print("Expense updated successfully.")
            else:
                print("Expense ID not found.")

        elif choice == "4":
            manager.show_expenses()

            expenses = manager.get_expenses()

            if not expenses:
                print("No expenses available to delete.")
                continue

            expense_id = int(input("Enter ID to delete: "))

            result = manager.delete_expense(expense_id)

            if result:
                print("Expense deleted successfully.")
            else:
                print("Expense ID not found.")

        elif choice == "5":
            manager.show_summary()

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()