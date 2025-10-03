from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ import CORS
import json, os

app = Flask(__name__)
CORS(app)  # ✅ allow frontend to talk to backend


# File to store expenses
DATA_FILE = "expenses.json"

# Load existing expenses or create empty list
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            expenses = json.load(f)
        except json.JSONDecodeError:
            expenses = []
else:
    expenses = []

def save_expenses():
    """Save expenses to file"""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Expense Tracker API!"})

@app.route("/expenses", methods=["GET"])
def get_expenses():
    """Return all expenses"""
    return jsonify(expenses)

@app.route("/expenses", methods=["POST"])
def add_expense():
    """Add a new expense"""
    data = request.json

    # Validate input
    if not data.get("name") or not data.get("amount") or not data.get("category") or not data.get("date"):
        return jsonify({"error": "Missing required fields"}), 400

    expense = {
        "name": data["name"],
        "amount": float(data["amount"]),
        "category": data["category"],
        "date": data["date"]
    }

    expenses.append(expense)
    save_expenses()

    return jsonify({"message": "Expense added successfully", "expense": expense}), 201

@app.route("/total", methods=["GET"])
def total_spent():
    """Return total spent"""
    total = sum(exp['amount'] for exp in expenses)
    return jsonify({"total_spent": total})

# Run app
if __name__ == "__main__":
    app.run(debug=True)
