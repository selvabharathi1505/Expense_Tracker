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
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            manager.add_expense()

        elif choice == "2":
            manager.show_expenses()

        elif choice == "3":
            manager.update_expense()

        elif choice == "4":
            manager.delete_expense()

        elif choice == "5":
            print("Program ended.")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()