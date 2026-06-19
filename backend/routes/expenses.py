from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Expense
from schemas import ExpenseCreate

router = APIRouter()

@router.post("/expenses")
def add_expense(data: ExpenseCreate, db: Session = Depends(get_db)):

    expense = Expense(
        user_id=data.user_id,
        amount=data.amount,
        category=data.category,
        description=data.description
    )

    db.add(expense)
    db.commit()

    return {"message": "Expense Added Successfully"}

@router.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).all()

    return expenses

@router.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    data: ExpenseCreate,
    db: Session = Depends(get_db)
):

    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    if not expense:
        return {"message": "Expense Not Found"}

    expense.user_id = data.user_id
    expense.amount = data.amount
    expense.category = data.category
    expense.description = data.description

    db.commit()

    return {"message": "Expense Updated Successfully"}

@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    if not expense:
        return {"message": "Expense Not Found"}

    db.delete(expense)
    db.commit()

    return {"message": "Expense Deleted Successfully"}