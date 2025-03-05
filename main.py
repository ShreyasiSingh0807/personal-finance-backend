from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# ✅ Database connection
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

# ✅ Create table if it doesn't exist
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

# ✅ Data model for expenses
class Expense(BaseModel):
    date: str
    category: str
    amount: float
    description: str

# ✅ API ROUTES

# ➤ **POST**: Add a new expense
@app.post("/expenses/")
def add_expense(expense: Expense):
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (expense.date, expense.category, expense.amount, expense.description))
    conn.commit()
    return {"message": "Expense added successfully!"}

# ➤ **GET**: Retrieve all expenses
@app.get("/expenses/")
def get_expenses():
    cursor.execute("SELECT id, date, category, amount, description FROM expenses")
    expenses = cursor.fetchall()
    return [{"id": e[0], "date": e[1], "category": e[2], "amount": e[3], "description": e[4]} for e in expenses]

# ➤ **DELETE**: Remove an expense by ID
@app.delete("/expenses/{expense_id}/")
def delete_expense(expense_id: int):
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    return {"message": "Expense deleted successfully!"}

