from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Allow frontend access (CORS enabled)

DATA_FILE = "expenses.json"

# Load existing expenses or create empty list
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        expenses = json.load(f)
else:
    expenses = []

def save_expenses():
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json
    try:
        expense = {
            "name": data["name"],
            "amount": float(data["amount"]),
            "category": data["category"],
            "date": data["date"]
        }
        expenses.append(expense)
        save_expenses()
        return jsonify({"message": "✅ Expense added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses)

@app.route("/total", methods=["GET"])
def total_spent():
    total = sum(exp["amount"] for exp in expenses)
    return jsonify({"total": total})

if __name__ == "__main__":
    app.run(debug=True)
