
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Database connection
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")
conn.commit()

# Pydantic model for expense input
class Expense(BaseModel):
    date: str
    category: str
    amount: float
    description: str

@app.post("/expenses/")
def add_expense(expense: Expense):
    cursor.execute(
        "INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
        (expense.date, expense.category, expense.amount, expense.description),
    )
    conn.commit()
    return {"message": "Expense added successfully"}

@app.get("/expenses/", response_model=List[Expense])
def get_expenses():
    cursor.execute("SELECT date, category, amount, description FROM expenses")
    expenses = cursor.fetchall()
    return [{"date": e[0], "category": e[1], "amount": e[2], "description": e[3]} for e in expenses]

@app.delete("/expenses/{expense_id}/")
def delete_expense(expense_id: int):
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    return {"message": "Expense deleted successfully"}

@app.get("/analytics/")
def get_analytics():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    return {"analytics": [{"category": d[0], "total_spent": d[1]} for d in data]}
