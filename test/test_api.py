
import os
import uuid
import pytest
import api

from datetime import date
from fastapi.testclient import TestClient
from expense_manager import ExpenseManager
from postgresql_storage import PostgreSQLStorage
from user_storage import UserStorage


@pytest.fixture
def client():
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

    with TestClient(api.app) as test_client:
        suffix = uuid.uuid4().hex[:10]

        registration = test_client.post(
            "/auth/register",
            json={
                "username": f"test_{suffix}",
                "email": f"test_{suffix}@example.com",
                "password": "TestPassword123"
            }
        )
        assert registration.status_code == 201, registration.text

        login = test_client.post(
            "/auth/login",
            json={
                "username": f"test_{suffix}",
                "password": "TestPassword123"
            }
        )
        assert login.status_code == 200, login.text

        token = login.json()["access_token"]
        test_client.headers.update({
            "Authorization": f"Bearer {token}"
        })

        yield test_client


def test_get_expenses(client):
    response = client.post("/expenses", json={
        "name": "Lunch", "category": "Food",
        "amount": 100, "date": "2026-09-02"
    })
    assert response.status_code == 201

    response = client.get("/expenses")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_expense(client):
    created = client.post("/expenses", json={
        "name": "Lunch", "category": "Food",
        "amount": 100, "date": "2026-09-02"
    })
    expense_id = created.json()["id"]

    response = client.get(f"/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Lunch"


def test_get_expense_not_found(client):
    response = client.get("/expenses/99999")
    assert response.status_code == 404


def test_create_expense(client):
    response = client.post("/expenses", json={
        "name": "Lunch", "category": "Food",
        "amount": 100, "date": "2026-09-02"
    })
    assert response.status_code == 201


def test_create_expense_response(client):
    response = client.post("/expenses", json={
        "name": "Dinner", "category": "Food",
        "amount": 200, "date": "2026-09-02"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Dinner"
    assert data["category"] == "Food"
    assert data["amount"] == 200
    assert data["date"] == "2026-09-02"


def test_update_expense(client):
    created = client.post("/expenses", json={
        "name": "Lunch", "category": "Food",
        "amount": 100, "date": "2026-09-02"
    })
    expense_id = created.json()["id"]

    response = client.put(f"/expenses/{expense_id}", json={
        "name": "Updated Lunch", "category": "Food",
        "amount": 150, "date": "2026-09-02"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Lunch"


def test_update_expense_not_found(client):
    response = client.put("/expenses/99999", json={
        "name": "Updated", "category": "Food",
        "amount": 150, "date": "2026-09-02"
    })
    assert response.status_code == 404


def test_delete_expense(client):
    created = client.post("/expenses", json={
        "name": "Dinner", "category": "Food",
        "amount": 100, "date": "2026-10-02"
    })
    expense_id = created.json()["id"]

    response = client.delete(f"/expenses/{expense_id}")
    assert response.status_code == 204


def test_delete_expense_not_found(client):
    response = client.delete("/expenses/99999")
    assert response.status_code == 404


def test_total_spending(client):
    client.post("/expenses", json={
        "name": "Lunch", "category": "Food",
        "amount": 100, "date": "2026-09-02"
    })
    client.post("/expenses", json={
        "name": "Dinner", "category": "Food",
        "amount": 200, "date": "2026-09-02"
    })

    response = client.get("/summary")
    assert response.status_code == 200
    assert response.json()["total_spending"] == 300


@pytest.mark.parametrize("amount", [-100, 0])
def test_create_expense_invalid_amount(client, amount):
    response = client.post("/expenses", json={
        "name": "Lunch", "category": "Food",
        "amount": amount, "date": "2026-09-02"
    })
    assert response.status_code == 422


def test_create_expense_missing_field(client):
    response = client.post("/expenses", json={
        "name": "Lunch", "amount": 100, "date": "2026-09-02"
    })
    assert response.status_code == 422


def test_create_expense_invalid_date(client):
    response = client.post("/expenses", json={
        "name": "Lunch", "category": "Food",
        "amount": 100, "date": "invalid-date"
    })
    assert response.status_code == 422


def test_create_expense_invalid_amount_type(client):
    response = client.post("/expenses", json={
        "name": "Lunch", "category": "Food",
        "amount": "hello", "date": "2026-09-02"
    })
    assert response.status_code == 422


def test_expenses_require_authentication():
    with TestClient(api.app) as unauthenticated_client:
        response = unauthenticated_client.get("/expenses")
        assert response.status_code == 401


def test_users_cannot_access_each_others_expenses(client):
    created = client.post("/expenses", json={
        "name": "Private expense", "category": "Food",
        "amount": 100, "date": "2026-09-02"
    })
    assert created.status_code == 201
    expense_id = created.json()["id"]

    # Register and log in as a second user.
    suffix = uuid.uuid4().hex[:10]
    username = f"other_{suffix}"
    password = "OtherPassword123"

    registration = client.post("/auth/register", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": password
    })
    assert registration.status_code == 201

    login = client.post("/auth/login", json={
        "username": username,
        "password": password
    })
    assert login.status_code == 200

    other_token = login.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {other_token}"})

    assert client.get("/expenses").json() == []
    assert client.get(f"/expenses/{expense_id}").status_code == 404

    update = client.put(f"/expenses/{expense_id}", json={
        "name": "Stolen update", "category": "Food",
        "amount": 150, "date": "2026-09-02"
    })
    assert update.status_code == 404

    assert client.delete(f"/expenses/{expense_id}").status_code == 404
