from fastmcp import FastMCP
import os
import sqlite3

mcp = FastMCP(name="expense_tracker")

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT NULL,
                note TEXT
            )
        ''')
        conn.commit()

init_db()

@mcp.tool
def add_expense(date: str, amount: float, category: str, subcategory: str|None = None, note: str|None = None):
    """Add a new expense entry"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (date, amount, category, subcategory, note)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, amount, category, subcategory, note))
        conn.commit()
    return {"status": "ok", id:cursor.lastrowid ,"message": "Expense added successfully"}

@mcp.tool
def list_expenses():
    """List all expense entries"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        rows = cursor.fetchall()
    expenses = [
        {
            "id": row[0],
            "date": row[1],
            "amount": row[2],
            "category": row[3],
            "subcategory": row[4],
            "note": row[5]
        }
        for row in rows
    ]
    return expenses

@mcp.tool
def delete_expense(expense_id: int):
    """Delete an expense entry by ID"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
    return {"status": "ok", "message": "Expense deleted successfully"}

@mcp.tool
def get_expense(expense_id: int):
    """Get details of a specific expense entry by ID"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
        row = cursor.fetchone()
    if row:
        expense = {
            "id": row[0],
            "date": row[1],
            "amount": row[2],
            "category": row[3],
            "subcategory": row[4],
            "note": row[5]
        }
        return expense
    else:
        return {"status": "error", "message": "Expense not found"}
    
@mcp.tool
def update_expense(expense_id: int, date: str|None = None, amount: float|None = None, category: str|None = None, subcategory: str|None = None, note: str|None = None):
    """Update an existing expense entry by ID"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        fields = []
        values = []
        if date is not None:
            fields.append("date = ?")
            values.append(date)
        if amount is not None:
            fields.append("amount = ?")
            values.append(amount)
        if category is not None:
            fields.append("category = ?")
            values.append(category)
        if subcategory is not None:
            fields.append("subcategory = ?")
            values.append(subcategory)
        if note is not None:
            fields.append("note = ?")
            values.append(note)
        values.append(expense_id)
        sql = f'UPDATE expenses SET {", ".join(fields)} WHERE id = ?'
        cursor.execute(sql, values)
        conn.commit()
    return {"status": "ok", "message": "Expense updated successfully"}

if __name__ == "__main__":
    mcp.run()