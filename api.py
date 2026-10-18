from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel, Field,EmailStr
from datetime import date, datetime, timedelta, timezone

from expense_manager import ExpenseManager
from postgresql_storage import PostgreSQLStorage
from user_storage import UserStorage

from fastapi.middleware.cors import CORSMiddleware
from pwdlib import PasswordHash
import psycopg
import jwt
import os
from dotenv import load_dotenv

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



load_dotenv()

app = FastAPI()

password_hash = PasswordHash.recommended()
user_storage = UserStorage()

oauth2_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            os.environ["SECRET_KEY"],
            algorithms=["HS256"],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return int(user_id)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

storage = PostgreSQLStorage()
manager = ExpenseManager(storage)

class ExpenseCreate(BaseModel):
    name: str
    category: str
    amount: float = Field(gt = 0)
    date: date


class ExpenseUpdate(BaseModel):
    name: str
    category: str
    amount: float = Field(gt = 0)
    date: date


class ExpenseResponse(BaseModel):
    id: int
    name: str
    category: str
    amount: float
    date: date
    
class SummaryResponse(BaseModel):
    total_spending: float
    category_wise: dict[str, float]



@app.post("/expenses", response_model=ExpenseResponse, status_code=201)
def create_expense(
    expense: ExpenseCreate,
    user_id: int = Depends(get_current_user),
):
    return manager.add_expense(
        expense.name, expense.category, expense.amount,
        expense.date, user_id
    )


@app.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(
    limit: int = 20,
    offset: int = 0,
    user_id: int = Depends(get_current_user),
):
    if limit < 1 or limit > 100 or offset < 0:
        raise HTTPException(status_code=422, detail="Invalid pagination")

    return manager.get_expenses(user_id, limit, offset)


@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    user_id: int = Depends(get_current_user),
):
    expense = manager.get_expense(expense_id, user_id)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense


@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    user_id: int = Depends(get_current_user),
):
    updated = manager.update_expense(
        expense_id, expense.name, expense.category,
        expense.amount, expense.date, user_id
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")

    return manager.get_expense(expense_id, user_id)


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(
    expense_id: int,
    user_id: int = Depends(get_current_user),
):
    deleted = manager.delete_expense(expense_id, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")


@app.get("/summary", response_model=SummaryResponse)
def get_summary(user_id: int = Depends(get_current_user)):
    return {
        "total_spending": manager.total_spending(user_id),
        "category_wise": manager.category_wise_spending(user_id),
    }




class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    
@app.post("/auth/register", status_code=201)
def register_user(user: UserRegister):
    if user_storage.username_or_email_exists(
        user.username, user.email
    ):
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    hashed_password = password_hash.hash(user.password)

    try:
        return user_storage.create_user(
            user.username,
            user.email,
            hashed_password,
        )
    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )
        
class UserLogin(BaseModel):
    username: str
    password: str
    


@app.post("/auth/login")
def login_user(user: UserLogin):
    db_user = user_storage.get_user_by_username(user.username)

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    if not password_hash.verify(
        user.password,
        db_user["password_hash"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    payload = {
        "sub": str(db_user["id"]),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }

    token = jwt.encode(
        payload,
        os.environ["SECRET_KEY"],
        algorithm="HS256",
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }