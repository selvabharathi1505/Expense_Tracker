from expense import Expense


def test_create_expense():
    expense = Expense(1, "Lunch", "Food", 20, "21/08/2026")

    assert expense.name == "Lunch"
    assert expense.category == "Food"
    assert expense.amount == 20
    assert expense.date == "21/08/2026"
    
from expense import Expense
from csv_storage import CSVStorage


def test_add_expense(tmp_path):
    file = tmp_path / "test_expenses.csv"
    storage = CSVStorage(file)
    expense = Expense(1,"Lunch","Food",20,"21/08/2026")
    storage.add(expense)
    expenses = storage.load()

    assert len(expenses) == 1
    assert expenses[0].name == "Lunch"
    assert expenses[0].category == "Food"
    assert expenses[0].amount == 20
    assert expenses[0].date == "21/08/2026"