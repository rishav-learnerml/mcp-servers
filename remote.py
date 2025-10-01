from fastmcp import FastMCP
import os
import sqlite3

mcp = FastMCP(name="expense_tracker")

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

def init_db():
    """Initialize the SQLite database and create the expenses table if it doesn't exist"""
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
    """Add a new expense entry
    
        Args:
            date (str): Date of the expense in YYYY-MM-DD format
            amount (float): Amount of the expense
            category (str): Category of the expense
            subcategory (str|None): Subcategory of the expense (optional)
            note (str|None): Additional note about the expense (optional)
        Returns:
            dict: Status message with the ID of the added expense
    """
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
    """List all expense entries
    
        Returns:
            list: List of all expense entries
    """
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
def list_expenses_in_range(start_date:str, end_date:str):
    """List all expense entries within a date range
    
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
        Returns:
            list: List of expense entries within the specified date range
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC""",(start_date,end_date))
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
    """Delete an expense entry by ID
    
        Args:
            expense_id (int): ID of the expense to delete
        Returns:
            dict: Status message
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
    return {"status": "ok", "message": "Expense deleted successfully"}

@mcp.tool
def get_expense(expense_id: int):
    """Get details of a specific expense entry by ID
    
        Args:
            expense_id (int): ID of the expense to retrieve
        Returns:
            dict: Expense details or error message
    """
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
    """Update an existing expense entry by ID

        Args:
            expense_id (int): ID of the expense to update
            date (str|None): New date in YYYY-MM-DD format (optional)
            amount (float|None): New amount (optional)
            category (str|None): New category (optional)
            subcategory (str|None): New subcategory (optional)
            note (str|None): New note (optional)
        Returns:
            dict: Status message
    """
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

@mcp.tool
def summarize(start_date:str, end_date:str, category:str|None=None):
    """Summarize expenses within a date range, optionally filtered by category
    
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            category (str|None): Category to filter by (optional)
        Returns:
            dict: Total expense amount
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if category:
            cursor.execute("""SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ? AND category = ?""",(start_date,end_date,category))
        else:
            cursor.execute("""SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?""",(start_date,end_date))
        total = cursor.fetchone()[0]
    return {"total_expense": total if total else 0}

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    """Get the list of expense categories from the categories.json file
    
        Returns:
            str: JSON string of categories
    """
    with open(CATEGORIES_PATH, "r" , encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000) ## For remote server, default transport is "stdio", we have changed it to "streamable http"