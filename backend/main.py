from fastapi import FastAPI
from database import engine
from models import Base
from routes.auth import router as auth_router
from routes.expenses import router as expense_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(expense_router)

@app.get("/")
def home():
    return {"message": "Expense Tracker API Running"}