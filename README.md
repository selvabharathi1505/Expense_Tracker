# Expense Tracker

A backend Expense Tracker application built with Python, FastAPI, PostgreSQL, and automated testing.

## Features

* Add expenses
* View expenses
* View a single expense by ID
* Update expenses
* Delete expenses
* View total spending
* View category-wise spending
* Pagination using `limit` and `offset`
* Input validation using Pydantic
* PostgreSQL database storage
* Separate PostgreSQL database for testing
* Automated API and unit tests

## Technologies Used

* Python
* FastAPI
* PostgreSQL
* Psycopg
* Pydantic
* Pytest
* Git & GitHub

## Project Structure

```text
Expense_Tracker/
│
├── api.py
├── expense.py
├── expense_manager.py
├── main.py
├── postgresql_storage.py
├── storage.py
├── requirements.txt
├── .env
├── .gitignore
│
└── test/
    ├── test_api.py
    └── test_expense_tracker.py
```

## API Endpoints

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| POST   | `/expenses`      | Create an expense    |
| GET    | `/expenses`      | Get expenses         |
| GET    | `/expenses/{id}` | Get expense by ID    |
| PUT    | `/expenses/{id}` | Update an expense    |
| DELETE | `/expenses/{id}` | Delete an expense    |
| GET    | `/summary`       | Get spending summary |

## Database

The application uses PostgreSQL.

Main database:

```text
expense_tracker
```

Test database:

```text
expense_tracker_test
```

The test database is kept separate so automated tests do not affect normal application data.

## API Validation

The API validates:

* Required fields
* Positive expense amounts
* Valid dates
* Correct data types

Invalid requests return appropriate HTTP validation errors.

## Testing

The project uses `pytest` for automated testing.

Tests cover:

* Adding expenses
* Getting expenses
* Getting an expense by ID
* Updating expenses
* Deleting expenses
* Non-existent expense IDs
* Total spending
* Category-wise spending
* API validation
* Invalid amounts
* Missing fields
* Invalid dates
* Invalid data types

Current test result:

```text
22 passed
```

Run tests with:

```bash
python -m pytest
```

## Running the API

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the PostgreSQL connection string in `.env`:

```env
DATABASE_URL=your_database_connection_string
```

Start the FastAPI application:

```bash
python -m uvicorn api:app --reload
```

API documentation is available through FastAPI Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

## Project Roadmap

* [x] Basic Expense Tracker
* [x] Interactive CLI
* [x] CSV Storage
* [x] Storage Abstraction
* [x] SQLite Storage
* [x] CLI Storage Selection
* [x] CRUD & Summaries
* [x] Unit Testing
* [x] FastAPI
* [x] API Testing & Validation
* [x] PostgreSQL
* [ ] Docker
* [ ] Web UI
* [ ] Authentication
* [ ] Deployment
* [ ] CI/CD
* [ ] AI Expense Assistant

```
