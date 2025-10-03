import json
import os

# File to store expenses
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

def personal_information():
    your_name = input("ENTER YOUR NAME: ")
    your_prefix = input("ENTER YOUR PREFIX (Mr./Mrs.): ")

    while True:
        try:
            age = int(input(f"{your_name}, ENTER YOUR AGE: "))
            break
        except ValueError:
            print("❌ Please enter a valid number for age!")

    if age >= 18:
        print("✅ You are eligible, You can go ahead!")
        return your_name, your_prefix
    else:
        print("🚫 You are not eligible. Please sign up with an adult.")
        exit()

def add_expense():
    name = input("Enter expense name: ")
    try:
        amount = float(input("Enter amount (in Rs.): "))
    except ValueError:
        print("❌ Invalid amount! Try again.")
        return
    category = input("Enter category (e.g., Food, Travel, Shopping, etc.): ")
    date = input("Enter date (DD-MM-YYYY): ")

    expense = {
        "name": name,
        "amount": amount,
        "category": category,
        "date": date
    }

    expenses.append(expense)
    save_expenses()
    print("✅ Expense added successfully!\n")

def view_expense():
    if not expenses:
        print("🚫 No expenses added yet!")
        return

    print("------- ALL EXPENSES -------")
    for i, expense in enumerate(expenses, start=1):
        print(f"{i}. {expense['date']} | {expense['name']} | {expense['category']} | Rs. {expense['amount']}")
    print()

def total_spent():
    total = sum(exp['amount'] for exp in expenses)
    print(f"💰 Your Total Expense is: Rs. {total}\n")

def run_tracker(your_name, your_prefix):
    print(f"\nWelcome {your_prefix} {your_name},")
    print("You're heartily welcomed to our 'Expense Tracker App'!\n")

    while True:
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total Spent")
        print("4. Exit\n")

        option = input("👉 Select an option (1 to 4): ")

        if option == "1":
            add_expense()
        elif option == "2":
            view_expense()
        elif option == "3":
            total_spent()
        elif option == "4":
            print("👋 Exiting the Expense Tracker App. Bye-bye!\n")
            break
        else:
            print("❌ Invalid option! Please choose between 1 and 4.\n")

# Run the app
if __name__ == "__main__":
    your_name, your_prefix = personal_information()
    run_tracker(your_name, your_prefix)
