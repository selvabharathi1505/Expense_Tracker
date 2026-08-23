from expense import Expense


def test_create_expense():
    expense = Expense(1, "Lunch", "Food", 20, "21/08/2026")

    assert expense.name == "Lunch"
    assert expense.category == "Food"
    assert expense.amount == 20
    assert expense.date == "21/08/2026"
    
