from expense import Expense
from expense_manager import ExpenseManager
from csv_storage import CSVStorage
from datetime import date

def test_total_spending(tmp_path):
    test_file = tmp_path / "test_expenses.csv"
    storage = CSVStorage(test_file)
    
    expense1 = Expense(1, "Lunch", "Food", 20, date(2026, 8, 23))
    storage.add(expense1)
    expense2 = Expense(2, "Uber", "Travel", 30, date(2026, 8, 23))
    storage.add(expense2)
    expense3 = Expense(3, "Dinner", "Food", 40, date(2026, 8, 23))
    storage.add(expense3)

    manager = ExpenseManager(storage)
    result = manager.total_spending()
    assert result == 90
    
def test_category_wise_spending(tmp_path):
    test_file = tmp_path / "test_expenses.csv"
    storage = CSVStorage(test_file)

    expense1 = Expense(1,"Lunch","Food",20,date(2026, 8, 23))
    expense2 = Expense(2,"Uber","Travel",30,date(2026, 8, 23))
    storage.add(expense1)
    storage.add(expense2)
    manager = ExpenseManager(storage)
    result = manager.category_wise_spending()
    assert result["Food"] == 20
    assert result["Travel"] == 30
    
def test_add_expense(tmp_path):
    test_file = tmp_path / "test_expenses.csv"
    storage = CSVStorage(test_file)

    manager = ExpenseManager(storage)
    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23))
    expenses = storage.load()

    assert len(expenses) == 1
    assert expenses[0].name == "Lunch"
    assert expenses[0].category == "Food"
    assert expenses[0].amount == 20
    assert expenses[0].date == date(2026, 8, 23)

def test_update_expense(tmp_path):
    test_file = tmp_path / "test_expenses.csv"
    storage = CSVStorage(test_file)

    expense1 = Expense(1, "Lunch", "Food", 20, date(2026, 8, 23))
    expense2 = Expense(2, "Uber", "Travel", 30, date(2026, 8, 23))
    expense3 = Expense(3, "Dinner", "Food", 40, date(2026, 8, 23))

    storage.add(expense1)
    storage.add(expense2)
    storage.add(expense3)

    manager = ExpenseManager(storage)

    result = manager.update_expense(2,"Uber","Travel",50,date(2026, 8, 23))

    assert result is True

    expenses = storage.load()

    assert expenses[1].name == "Uber"
    assert expenses[1].amount == 50

    
def test_update_nonexistent_expense(tmp_path):
    test_file = tmp_path / "test_expenses.csv"
    storage = CSVStorage(test_file)

    expense1 = Expense(1,"Lunch","Food",20,date(2026, 8, 23))
    storage.add(expense1)

    manager = ExpenseManager(storage)
    result = manager.update_expense(99,"Dinner","Food",40,date(2026, 8, 23))

    assert result is False
    expenses = storage.load()

    assert len(expenses) == 1
    assert expenses[0].name == "Lunch"
    assert expenses[0].amount == 20
    
    
def test_delete_expense(tmp_path):
    test_file = tmp_path / "test_expenses.csv"
    storage = CSVStorage(test_file)

    expense1 = Expense(1,"Lunch","Food",20,date(2026, 8, 23))
    expense2 = Expense(2,"Uber","Travel",30,date(2026, 8, 23))
    expense3 = Expense(3,"Dinner","Food",40,date(2026, 8, 23))

    storage.add(expense1)
    storage.add(expense2)
    storage.add(expense3)

    manager = ExpenseManager(storage)

    result = manager.delete_expense(1)
    assert result is True
    expenses = storage.load()

    assert len(expenses) == 2
    assert expenses[0].name == "Uber"
    assert expenses[1].name == "Dinner"
    
    
def test_delete_nonexistent_expense(tmp_path):
    test_file = tmp_path / "test_expenses.csv"
    storage = CSVStorage(test_file)
    
    expense1 = Expense(1,"Lunch","Food",20,date(2026, 8, 23))
    storage.add(expense1)
    
    manager = ExpenseManager(storage)

    result = manager.delete_expense(99)

    assert result is False
    
    expenses = storage.load()
    assert len(expenses) == 1
    assert expenses[0].name == "Lunch"
    assert expenses[0].amount == 20