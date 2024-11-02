import datetime
import json
import os

# Expense Tracker
class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.load_data()

    def load_data(self):
        # Load expenses from a file, or initialize an empty list if file doesn't exist
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.expenses = json.load(file)
        else:
            self.expenses = []

    def save_data(self):
        # Save expenses to a file
        with open(self.filename, "w") as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, amount, category, description=""):
        # Add an expense entry
        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.expenses.append(expense)
        self.save_data()
        print(f"Added: {expense}")

    def view_expenses(self, category=None):
        # View expenses, filtered by category if specified
        filtered_expenses = [e for e in self.expenses if category is None or e["category"] == category]
        if not filtered_expenses:
            print("No expenses found.")
            return
        for expense in filtered_expenses:
            print(expense)

    def analyze_expenses(self):
        # Summarize expenses by category
        summary = {}
        for expense in self.expenses:
            category = expense["category"]
            summary[category] = summary.get(category, 0) + expense["amount"]
        
        print("\nExpense Summary by Category:")
        for category, total in summary.items():
            print(f"{category}: ${total:.2f}")

# Main program
def main():
    tracker = ExpenseTracker()

    while True:
        print("\nOptions: (1) Add Expense, (2) View Expenses, (3) Analyze Expenses, (4) Quit")
        choice = input("Choose an option: ")

        if choice == '1':
            try:
                amount = float(input("Enter amount: $"))
                category = input("Enter category (e.g., Food, Rent, Transport): ")
                description = input("Enter description (optional): ")
                tracker.add_expense(amount, category, description)
            except ValueError:
                print("Invalid amount entered. Please try again.")
        
        elif choice == '2':
            category = input("Enter category to filter by (leave blank for all): ")
            tracker.view_expenses(category or None)

        elif choice == '3':
            tracker.analyze_expenses()
        
        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
