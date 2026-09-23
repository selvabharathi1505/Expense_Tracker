import pytest
import os
from datetime import date
from expense_manager import ExpenseManager
from postgresql_storage import PostgreSQLStorage

@pytest.fixture
def manager():
    storage = PostgreSQLStorage(os.getenv("TEST_DATABASE_URL"))
    conn = storage.get_connection()
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE expenses RESTART IDENTITY")
    conn.commit()
\
    cursor.close()
    conn.close()

    return ExpenseManager(storage)

def test_total_spending(manager):
    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23))
    manager.add_expense("Uber", "Travel", 30, date(2026, 8, 23))
    manager.add_expense("Dinner", "Food", 40, date(2026, 8, 23))
    result = manager.total_spending()

    assert result == 90

def test_category_wise_spending(manager):
    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23))
    manager.add_expense("Uber", "Travel", 30, date(2026, 8, 23))
    result = manager.category_wise_spending()

    assert result["Food"] == 20
    assert result["Travel"] == 30

def test_add_expense(manager):
    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23))
    expenses = manager.get_expenses()

    assert len(expenses) == 1
    assert expenses[0].name == "Lunch"
    assert expenses[0].category == "Food"
    assert expenses[0].amount == 20
    assert expenses[0].date == date(2026, 8, 23)

def test_update_expense(manager):
    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23))
    result = manager.update_expense(1,"Updated Lunch","Food",50,date(2026, 8, 23))
    assert result is True
    expense = manager.get_expense(1)
    assert expense.name == "Updated Lunch"
    assert expense.amount == 50

def test_update_nonexistent_expense(manager):
    result = manager.update_expense(99,"Dinner","Food",40,date(2026, 8, 23))
    assert result is False

def test_delete_expense(manager):
    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23))
    result = manager.delete_expense(1)
    assert result is True
    assert manager.get_expense(1) is None


def test_delete_nonexistent_expense(manager):
    result = manager.delete_expense(99)
    assert result is False