from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.auth.router import router as auth_router
from app.routes.expenses import router as expenses_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Group Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(expenses_router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}