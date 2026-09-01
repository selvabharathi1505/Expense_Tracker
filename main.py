from csv_storage import CSVStorage
from sqlite_storage import SQLiteStorage
from expense_manager import ExpenseManager
import argparse


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--storage",
        choices=["csv", "sqlite"],
        required=True,
        help="Choose storage type: csv or sqlite"
    )

    args = parser.parse_args()

    if args.storage == "csv":
        print("Using CSV Storage")
        storage = CSVStorage()

    elif args.storage == "sqlite":
        print("Using SQLite Storage")
        storage = SQLiteStorage()

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
                date = input("Enter Date (dd/mm/yyyy): ")

                manager.add_expense(name,category,amount,date)
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
            date = input("Enter new Date: ")

            result = manager.update_expense(expense_id,name,category,amount,date)

            if result:
                print("Expense updated successfully.")
            else:
                print("Expense ID not found")

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
                print("Expense ID not found")


        elif choice == "5":
            manager.show_summary()
            
        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()