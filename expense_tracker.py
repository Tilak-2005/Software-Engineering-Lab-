# //before

# import os
# import tempfile
# from datetime import datetime

# BANK_SYNC_PASSWORD = "demo-sync-pass"
# expenses = []
# monthly_budget = 20000
# REPORT_DIR = "/tmp/expense_reports"


# def addExpense(amount, category="Misc", note=""):
#     if amount <= 0:
#         print("Ignoring invalid amount", amount)
#         return False
#     expenses.append({"amount" : amount, "category": category,
#                      "note": note, "time": datetime.now().isoformat()})
#     return True


# def totalByCategory():
#     totals = {}
#     for expense in expenses:
#         category = expense["category"]
#         totals[category] = totals.get(category, 0) + expense["amount"]
#     return totals


# def setBudget(newBudget):
#     global monthly_budget
#     monthly_budget = newBudget


# def remainingBudget():
#     spent = sum(expense["amount"] for expense in expenses)
#     return monthly_budget - spent


# def biggestExpense():
#     try:
#         return max(expenses, key=lambda expense: expense["amount"])
#     except Exception:
#         return None

# def printLedger():
#     for i in range(len(expenses)):
#         print(i + 1, expenses[i]["category"], expenses[i]["amount"])


# def checkSyncPassword(password):
#     return password == BANK_SYNC_PASSWORD


# def exportReport():
#     # Helper kept for the lab: not called by the demo
#     reportPath = tempfile.mktemp(suffix=".txt", dir=REPORT_DIR)
#     return reportPath


# def openStatement(path):
#     # Helper kept for the lab: not called by the demo
#     os.system("xdg-open " + path)


# def main():
#     print("Biggest expense before any entries:", biggestExpense())
#     addExpense(450, "Food", "Lunch with team")
#     addExpense(1200, "Travel", "Cab to airport")
#     addExpense(-50, "Food")
#     addExpense(300, "Food", "Groceries")
#     addExpense(999, "Bills", "Internet")
#     setBudget(5000)
#     printLedger()
#     print("Totals:", totalByCategory())
#     print("Remaining budget:", remainingBudget()) # after setBudget
#     print("Biggest expense:", biggestExpense()["note"])
#     print("Sync password accepted:", checkSyncPassword("guess"))
#     print("Summary:", len(expenses), "expenses recorded against a budget of", monthly_budget)


# main()


"""Expense tracker for recording expenses and managing a monthly budget."""

import os
import tempfile
from datetime import datetime
import webbrowser
from pathlib import Path

BANK_SYNC_PASSWORD = os.getenv("BANK_SYNC_PASSWORD")
expenses = []
MONTHLY_BUDGET = 20000
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")


def add_expense(amount, category="Misc", note=""):
    """Add an expense to the ledger if the amount is valid."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False

    expenses.append({
        "amount": amount,
        "category": category,
        "note": note,
        "time": datetime.now().isoformat(),
    })
    return True


def total_by_category():
    """Calculate total expenses for each category."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Validate and return the new monthly budget."""
    if new_budget < 0:
        raise ValueError("Budget cannot be negative.")
    return new_budget


def remaining_budget(budget):
    """Calculate the remaining budget after expenses."""
    spent = sum(expense["amount"] for expense in expenses)
    return budget - spent


def biggest_expense():
    """Return the largest expense, or None if no expenses exist."""
    try:
        return max(expenses, key=lambda expense: expense["amount"])
    except ValueError:
        return None


def print_ledger():
    """Print all expenses with their sequence numbers."""
    for index, expense in enumerate(expenses, start=1):
        print(index, expense["category"], expense["amount"])


def check_sync_password(password):
    """Check whether the supplied password matches the configured password."""
    return bool(BANK_SYNC_PASSWORD) and password == BANK_SYNC_PASSWORD


def export_report():
    """Create a report file securely and return its path."""
    os.makedirs(REPORT_DIR, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        prefix="expense_report_",
        dir=REPORT_DIR,
        delete=False,
        encoding="utf-8",
    ) as report_file:
        for expense in expenses:
            report_file.write(
                f"{expense['category']}: {expense['amount']}\n"
            )

        return report_file.name





def open_statement(path):
    """Open an existing report using the default browser."""
    report_path = Path(path).resolve()

    if not report_path.is_file():
        raise FileNotFoundError(f"Report not found: {report_path}")

    webbrowser.open(report_path.as_uri())


def main():
    """Run the expense tracker demonstration."""
    monthly_budget = MONTHLY_BUDGET

    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")

    monthly_budget = set_budget(5000)

    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget(monthly_budget))
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:",
        len(expenses),
        "expenses recorded against a budget of",
        monthly_budget,
    )


if __name__ == "__main__":
    main()

