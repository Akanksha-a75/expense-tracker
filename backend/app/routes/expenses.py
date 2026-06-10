from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseResponse
from app.auth.session import verify_token
from typing import List, Optional
from datetime import date

router = APIRouter()

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload  # this is the email

@router.post("/expenses/add")
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    from app.models import User
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_expense = Expense(
        user_id=user.id,
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        description=expense.description
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return {"message": "Expense added successfully", "expense_id": new_expense.id}

@router.get("/expenses/list", response_model=List[ExpenseResponse])
def list_expenses(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    from app.models import User
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    expenses = db.query(Expense).filter(Expense.user_id == user.id).all()
    return expenses

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    from app.models import User
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

@router.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    from app.models import User
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user.id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    existing.amount = expense.amount
    existing.category = expense.category
    existing.date = expense.date
    existing.description = expense.description
    db.commit()
    db.refresh(existing)
    return existing