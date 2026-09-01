from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from expense_manager import ExpenseManager
from csv_storage import CSVStorage


app = FastAPI()

storage = CSVStorage("expenses.csv")
manager = ExpenseManager(storage)


class ExpenseCreate(BaseModel):
    name: str
    category: str
    amount: float
    date: str


class ExpenseUpdate(BaseModel):
    name: str
    category: str
    amount: float
    date: str


class ExpenseResponse(BaseModel):
    id: int
    name: str
    category: str
    amount: float
    date: str
    
class SummaryResponse(BaseModel):
    total_spending: float
    category_wise: dict[str, float]


@app.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses():
    return manager.get_expenses()


@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):
    expense = manager.get_expense(expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense


@app.post("/expenses", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate):
    return manager.add_expense(
        expense.name,
        expense.category,
        expense.amount,
        expense.date
    )


@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseUpdate):

    result = manager.update_expense(
        expense_id,
        expense.name,
        expense.category,
        expense.amount,
        expense.date
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return manager.get_expense(expense_id)


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):

    result = manager.delete_expense(expense_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
        
        
@app.get("/summary", response_model=SummaryResponse)
def get_summary():
    return {
        "total_spending": manager.total_spending(),
        "category_wise": manager.category_wise_spending()
    }