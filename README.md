# Expense Tracker

A Python-based command-line Expense Tracker that allows users to **add, view, update, and delete expenses**.

The application supports two storage methods:

* **CSV file storage**
* **SQLite database storage**

The storage method can be selected when running the application through a command-line argument.

## Features

* Add one or multiple expenses
* View all stored expenses
* Update an existing expense using its ID
* Delete an expense using its ID
* Store data using CSV
* Store data using SQLite
* Common storage interface using an abstract base class
* Command-line storage selection using `sys.argv`
* Object-oriented design

## Technologies Used

* **Python 3**
* **CSV**
* **SQLite**
* **Object-Oriented Programming (OOP)**
* **Abstract Base Class (ABC)**
* **Command-Line Arguments**
* **Git & GitHub**

## Project Structure

```text
Expense_Tracker/
│
├── main.py
├── expense.py
├── expense_manager.py
├── storage.py
├── csv_storage.py
├── sqlite_storage.py
├── expenses.csv
├── expenses.db
├── .gitignore
└── README.md
```

### File Description

| File                 | Description                                   |
| -------------------- | --------------------------------------------- |
| `main.py`            | Application entry point and storage selection |
| `expense.py`         | Defines the Expense object                    |
| `expense_manager.py` | Contains expense management operations        |
| `storage.py`         | Defines the common Storage interface          |
| `csv_storage.py`     | Implements storage using a CSV file           |
| `sqlite_storage.py`  | Implements storage using SQLite               |
| `expenses.csv`       | CSV data file                                 |
| `expenses.db`        | SQLite database file                          |
| `.gitignore`         | Prevents unnecessary files from being tracked |

## Architecture

The project follows a common storage interface design:

```text
                         main.py
                            |
                            v
                      ExpenseManager
                            |
                            v
                       Storage (ABC)
                        /        \
                       /          \
                      v            v
                CSVStorage     SQLiteStorage
                   |              |
                   v              v
             expenses.csv     expenses.db
```

The `Storage` abstract base class defines common operations such as:

* `load()`
* `add()`
* `update()`
* `delete()`

Both `CSVStorage` and `SQLiteStorage` implement these operations. This allows `ExpenseManager` to work with either storage method without changing its main logic.

## Requirements

* Python 3.x
* No external Python packages are required.

The project uses Python's built-in `csv`, `sqlite3`, `abc`, and `sys` modules.

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/selvabharathi1505/Expense_Tracker.git
```

### 2. Navigate to the Project Directory

```bash
cd Expense_Tracker
```

### 3. Select the Storage Method

The storage method is selected using a command-line argument.

#### CSV Storage

Use **`1`** for CSV storage:

```bash
python main.py 1
```

Output:

```text
Using CSV Storage
```

**`1 = CSV Storage`**

#### SQLite Storage

Use **`2`** for SQLite storage:

```bash
python main.py 2
```

Output:

```text
Using SQLite Storage
```

**`2 = SQLite Storage`**

### Quick Reference

| Command            | Storage Method |
| ------------------ | -------------- |
| `python main.py 1` | CSV            |
| `python main.py 2` | SQLite         |

## Expense Menu

After selecting the storage method, the application displays:

```text
1. Add Expense
2. Show Expenses
3. Update Expense
4. Delete Expense
5. Exit
```

### 1. Add Expense

Select option `1` to add expenses.

The application asks for:

* Number of expenses
* Name
* Category
* Amount
* Date

Example:

```text
Enter how many expenses to be added: 1

Enter the details for expense 1:
Enter Name: Lunch
Enter Category: Food
Enter Amount: 150
Enter Date (dd/mm/yyyy): 18/08/2026
```

### 2. Show Expenses

Select option `2` to display the stored expenses.

### 3. Update Expense

Select option `3` and provide the expense ID.

The application allows you to update:

* Name
* Category
* Amount
* Date

### 4. Delete Expense

Select option `4` and provide the expense ID to delete the expense.

### 5. Exit

Select option `5` to close the application.

## CSV Storage

When you run:

```bash
python main.py 1
```

the application uses `CSVStorage`.

Expenses are stored in:

```text
expenses.csv
```

The CSV file contains:

```text
id,name,category,amount,date
```

CSV storage provides a simple file-based approach for storing expense records.

## SQLite Storage

When you run:

```bash
python main.py 2
```

the application uses `SQLiteStorage`.

Expenses are stored in:

```text
expenses.db
```

The SQLite database contains an `expenses` table with the following fields:

```text
id
name
category
amount
date
```

SQLite provides structured database operations for adding, retrieving, updating, and deleting individual expense records.

## CSV vs SQLite

| Feature                      | CSV                                | SQLite                     |
| ---------------------------- | ---------------------------------- | -------------------------- |
| Storage type                 | File                               | Database                   |
| File                         | `expenses.csv`                     | `expenses.db`              |
| Structured queries           | Limited                            | Supported                  |
| Individual record operations | Implemented through file rewriting | Database operations        |
| Setup                        | Very simple                        | Very simple                |
| Best suited for              | Simple/small data                  | Structured data management |

## Object-Oriented Design

The project separates responsibilities into different classes.

### Expense

Represents an individual expense containing:

* ID
* Name
* Category
* Amount
* Date

### ExpenseManager

Handles the application's expense operations:

* Add
* Show
* Update
* Delete

### Storage

Defines the common interface that storage implementations must follow.

### CSVStorage

Handles reading and writing expenses using a CSV file.

### SQLiteStorage

Handles expense records using an SQLite database.

This separation makes the project easier to maintain and allows different storage implementations to be used with the same `ExpenseManager`.

## Example

Run the application with CSV:

```bash
python main.py 1
```

Then:

```text
Using CSV Storage

1. Add Expense
2. Show Expenses
3. Update Expense
4. Delete Expense
5. Exit

Enter choice: 1
```

To use SQLite instead:

```bash
python main.py 2
```

## Future Improvements

Possible future enhancements include:

* Add expense search and filtering
* Add monthly and category-wise expense summaries
* Add total expense calculation
* Add graphical user interface (GUI)
* Add data visualization
* Add input validation

## Learning Objectives

This project demonstrates practical use of:

* Python classes and objects
* Abstraction
* Abstract base classes
* Inheritance
* File handling
* CSV handling
* SQLite database operations
* Command-line arguments
* Separation of concerns
* Interface-based design

## Author

**Selvabharathi S**

## Repository

[Expense Tracker on GitHub](https://github.com/selvabharathi1505/Expense_Tracker)

## License

This project is created for educational and portfolio purposes.
