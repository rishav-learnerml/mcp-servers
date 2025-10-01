# 💸 MCP Expense Tracker

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.12%2B-purple?logo=fastapi)](https://github.com/robusta-dev/fastmcp)
[![Remote MCP Server](https://img.shields.io/badge/Remote%20MCP-Live-green?logo=cloudflare)](https://smart-expense-tracker.fastmcp.app/mcp)

---

> **Track your expenses locally or remotely with blazing-fast MCP tools!**

---

## 🚀 Live Remote MCP Server

🌐 **Try it now:** [https://smart-expense-tracker.fastmcp.app/mcp](https://smart-expense-tracker.fastmcp.app/mcp)

---

## 🖼️ Preview

<!--
Add screenshots or diagrams here!
Example:
![Expense Tracker Screenshot](assets/screenshot.png)
-->

---

## ✨ Features

- 📦 **Local & Remote MCP Server**
- 📝 Add, list, update, and delete expenses
- 📊 Summarize expenses by date and category
- 🗂️ Rich category & subcategory support (see below)
- 🔒 SQLite database for fast, secure storage
- ⚡ Powered by [FastMCP](https://github.com/robusta-dev/fastmcp) & FastAPI

---

## ⚡ Quick Start (Local)

```bash
# 1. Clone this repo
$ git clone <your-repo-url>
$ cd mcp-servers

# 2. Install dependencies
$ pip install -r requirements.txt

# 3. Run the local MCP server
$ python main.py
```

---

## ☁️ Remote MCP Server Usage

You can use the remote MCP server instantly:

- **Endpoint:** `https://smart-expense-tracker.fastmcp.app/mcp`
- Compatible with any MCP client or tool that supports remote endpoints.

---

## 🛠️ API Tools Overview

| Tool Name                | Description                         |
| ------------------------ | ----------------------------------- |
| `add_expense`            | Add a new expense entry             |
| `list_expenses`          | List all expense entries            |
| `list_expenses_in_range` | List expenses within a date range   |
| `delete_expense`         | Delete an expense by ID             |
| `get_expense`            | Get details of a specific expense   |
| `update_expense`         | Update an existing expense          |
| `summarize`              | Summarize expenses by date/category |
| `categories`             | Get all available categories (JSON) |

---

## 🗂️ Categories & Subcategories

Your expenses are organized into rich categories and subcategories, including:

- **Food:** groceries, restaurants, coffee, snacks, drinks, fast food, ...
- **Transportation:** public transit, taxi, fuel, parking, ...
- **Utilities:** electricity, water, internet, ...
- **Entertainment:** movies, concerts, streaming, ...
- **Health:** doctor, gym, medications, ...
- **Shopping:** clothing, electronics, gifts, ...
- **Travel:** flights, hotels, vacation, ...
- **Education:** tuition, books, courses, ...
- **Personal Care:** haircuts, spa, skincare, ...
- **Miscellaneous, Investments, Housing** and more!

See `categories.json` for the full list.

---

## 🏗️ Tech Stack

- **Python 3.13+**
- **FastMCP**
- **FastAPI**
- **Uvicorn**
- **SQLite**

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License. See `LICENSE` file for details.

---

> Made with ❤️ using FastMCP & Python
