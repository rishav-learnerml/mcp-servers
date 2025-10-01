from fastmcp import FastMCP

mcp = FastMCP.as_proxy("https://smart-expense-tracker.fastmcp.app/mcp",name="expense_tracker_proxy")

if __name__ == "__main__":
    mcp.run()  # starts the proxy server