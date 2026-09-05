import pytest
import api
from fastapi.testclient import TestClient
from expense_manager import ExpenseManager
from csv_storage import CSVStorage
from sqlite_storage import SQLiteStorage
from datetime import date

@pytest.fixture(params=["csv", "sqlite"])
def client(request, tmp_path):

    if request.param == "csv":
        test_file = tmp_path / "test_expenses.csv"
        storage = CSVStorage(test_file)

    elif request.param == "sqlite":
        test_file = tmp_path / "test_expenses.db"
        storage = SQLiteStorage(test_file)

    api.manager = ExpenseManager(storage)

    return TestClient(api.app)


def test_get_expenses(client):
    api.manager.add_expense("Lunch","Food",100,date(2026, 9, 2))
    
    response = client.get("/expenses")

    assert response.status_code == 200

def test_get_expense(client):
    api.manager.add_expense("Lunch","Food",100,date(2026, 9, 2))
    response = client.get("/expenses/1")

    assert response.status_code == 200

def test_get_expense_not_found(client):
    response = client.get("/expenses/99999")

    assert response.status_code == 404

def test_create_expense(client):
    response = client.post("/expenses",
        json={
            "name": "Lunch",
            "category": "Food",
            "amount": 100,
            "date": "2026-09-02"
        }
    )

    assert response.status_code == 201

def test_create_expense_response(client):
    response = client.post(
        "/expenses",
        json={
            "name": "Dinner",
            "category": "Food",
            "amount": 200,
            "date": "2026-09-02"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Dinner"
    assert data["category"] == "Food"
    assert data["amount"] == 200
    assert data["date"] == "2026-09-02"

def test_update_expense(client):
    api.manager.add_expense("Lunch","Food",100,date(2026, 9, 2))
    response = client.put("/expenses/1",
        json={
            "name": "Updated Lunch",
            "category": "Food",
            "amount": 150,
            "date": "2026-09-02"
        }
    )

    assert response.status_code == 200
    
def test_update_expense_not_found(client):
    response = client.put("/expenses/999",
        json={
            "name": "Updated",
            "category": "Food",
            "amount": 150,
            "date": "2026-09-02"
        }
    )

    assert response.status_code == 404
    
def test_delete_expense(client):
    api.manager.add_expense("Dinner","Food",100,date(2026, 10, 2))
    response = client.delete("/expenses/1")

    assert response.status_code == 204
    
def test_delete_expense_not_found(client):
    response = client.delete("/expenses/99999")

    assert response.status_code == 404
    
def test_total_spending(client):
    api.manager.add_expense("Lunch","Food",100,date(2026, 9, 2))
    api.manager.add_expense("Dinner","Food",200,date(2026, 9, 2))

    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_spending"] == 300