
import os
import pytest
import api

from datetime import date
from fastapi.testclient import TestClient
from expense_manager import ExpenseManager
from postgresql_storage import PostgreSQLStorage
from user_storage import UserStorage


@pytest.fixture
def manager():
    database_url = os.getenv("TEST_DATABASE_URL")
    if not database_url:
        pytest.fail("TEST_DATABASE_URL is not configured")

    storage = PostgreSQLStorage(database_url)
    conn = storage.get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE expenses, users RESTART IDENTITY CASCADE")
        conn.commit()
    finally:
        conn.close()

    api.user_storage = UserStorage(database_url)
    api.manager = ExpenseManager(storage)

    with TestClient(api.app) as client:
        response = client.post(
            "/auth/register",
            json={
                "username": "tracker_test_user",
                "email": "tracker_test@example.com",
                "password": "TestPassword123"
            }
        )
        assert response.status_code == 201, response.text

        user_id = response.json()["id"]

        manager = ExpenseManager(storage)
        manager.test_user_id = user_id
        yield manager


def test_total_spending(manager):
    user_id = manager.test_user_id

    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23), user_id)
    manager.add_expense("Uber", "Travel", 30, date(2026, 8, 23), user_id)
    manager.add_expense("Dinner", "Food", 40, date(2026, 8, 23), user_id)

    assert manager.total_spending(user_id) == 90


def test_category_wise_spending(manager):
    user_id = manager.test_user_id

    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23), user_id)
    manager.add_expense("Uber", "Travel", 30, date(2026, 8, 23), user_id)

    result = manager.category_wise_spending(user_id)

    assert result["Food"] == 20
    assert result["Travel"] == 30


def test_add_expense(manager):
    user_id = manager.test_user_id

    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23), user_id)
    expenses = manager.get_expenses(user_id)

    assert len(expenses) == 1
    assert expenses[0].name == "Lunch"
    assert expenses[0].category == "Food"
    assert expenses[0].amount == 20
    assert expenses[0].date == date(2026, 8, 23)


def test_update_expense(manager):
    user_id = manager.test_user_id

    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23), user_id)

    result = manager.update_expense(
        1, "Updated Lunch", "Food", 50, date(2026, 8, 23), user_id
    )

    assert result is True

    expense = manager.get_expense(1, user_id)
    assert expense.name == "Updated Lunch"
    assert expense.amount == 50


def test_update_nonexistent_expense(manager):
    result = manager.update_expense(
        999, "Dinner", "Food", 40, date(2026, 8, 23),
        manager.test_user_id
    )

    assert result is False


def test_delete_expense(manager):
    user_id = manager.test_user_id

    manager.add_expense("Lunch", "Food", 20, date(2026, 8, 23), user_id)

    result = manager.delete_expense(1, user_id)

    assert result is True
    assert manager.get_expense(1, user_id) is None


def test_delete_nonexistent_expense(manager):
    result = manager.delete_expense(999, manager.test_user_id)

    assert result is False
