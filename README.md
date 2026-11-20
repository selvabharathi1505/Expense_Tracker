# 💰 Expense Tracker

A full-stack Expense Tracker application built using **Python, FastAPI, PostgreSQL, HTML, CSS, and JavaScript**.

The application allows users to manage their personal expenses securely with JWT authentication, expense summaries, and CRUD operations.

## 🚀 Features

- User Registration and Login
- JWT-based Authentication
- User-specific Expense Management
- Add New Expenses
- View All Expenses
- Update Existing Expenses
- Delete Expenses
- Category-wise Expense Summary
- Total Spending Calculation
- PostgreSQL Database Integration
- RESTful API Architecture
- Frontend and Backend Integration

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| FastAPI | REST API Development |
| PostgreSQL | Database |
| HTML | Frontend Structure |
| CSS | Frontend Styling |
| JavaScript | Frontend Functionality |
| JWT | Authentication |
| Git & GitHub | Version Control |

## 📂 Project Structure

```text
expense_manager/
│
├── api.py
├── app.py
├── expense.py
├── expense_manager.py
├── storage.py
├── postgresql_storage.py
├── user_storage.py
│
├── tests/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/selvabharathi1505/Expense_Tracker.git
```

### 2. Navigate to the Project

```bash
cd Expense_Tracker
```

### 3. Create a Virtual Environment

```bash
python -m venv env
```

### 4. Activate Virtual Environment

Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
```

Never commit your `.env` file to GitHub.

### 7. Run the Application

```bash
python -m uvicorn api:app --reload
```

### 8. Access the API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

## 🔐 Authentication

The application uses JWT-based authentication.

- Users can register and log in.
- Successful login generates an access token.
- Protected endpoints require a valid token.
- Each user can access only their own expenses.

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | User login |
| GET | `/expenses` | Get user expenses |
| GET | `/expenses/{id}` | Get expense by ID |
| POST | `/expenses` | Add an expense |
| PUT | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |
| GET | `/summary` | Get expense summary |

## 🧪 Testing

Run the test suite:

```bash
python -m pytest -v
```

## 🎯 Project Goals

This project demonstrates practical implementation of:

- Object-Oriented Programming
- Clean Backend Architecture
- REST API Development
- Database Integration
- Authentication and Authorization
- Frontend and Backend Communication
- Unit Testing
- Version Control

## 🔮 Future Improvements

- Docker Containerization
- Cloud Deployment
- Improved UI/UX
- Advanced Expense Analytics
- Monthly and Yearly Reports

## 👨‍💻 Developer

**Selvabharathi S**

B.Tech Graduate | Aspiring Software Developer

GitHub: https://github.com/selvabharathi1505

---

⭐ If you find this project interesting, consider giving it a star!
