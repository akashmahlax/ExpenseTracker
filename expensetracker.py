import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# Expense Tracker App with GUI
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("400x500")
        self.root.configure(bg="#e0f7fa")

        self.filename = "expenses.json"
        self.expenses = self.load_data()

        # Header
        tk.Label(root, text="Expense Tracker", font=("Helvetica", 18, "bold"), bg="#00796b", fg="white").pack(fill="x")

        # Add Expense Frame
        self.add_expense_frame = tk.Frame(root, bg="#e0f7fa", pady=10)
        self.add_expense_frame.pack(fill="x", padx=20)

        tk.Label(self.add_expense_frame, text="Amount ($):", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=0, column=0, pady=5, sticky="w")
        self.amount_entry = tk.Entry(self.add_expense_frame, width=20)
        self.amount_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(self.add_expense_frame, text="Category:", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=1, column=0, pady=5, sticky="w")
        self.category_entry = tk.Entry(self.add_expense_frame, width=20)
        self.category_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self.add_expense_frame, text="Description:", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=2, column=0, pady=5, sticky="w")
        self.description_entry = tk.Entry(self.add_expense_frame, width=20)
        self.description_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Button(self.add_expense_frame, text="Add Expense", command=self.add_expense, bg="#00796b", fg="white", font=("Helvetica", 12)).grid(row=3, columnspan=2, pady=10)

        # View Expenses Frame
        self.expenses_frame = tk.Frame(root, bg="#e0f7fa")
        self.expenses_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.view_expenses()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        return []

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get().strip()
            description = self.description_entry.get().strip()
            if not category:
                raise ValueError("Category is required.")
            expense = {
                "amount": amount,
                "category": category,
                "description": description,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.expenses.append(expense)
            self.save_data()
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.view_expenses()
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def view_expenses(self):
        for widget in self.expenses_frame.winfo_children():
            widget.destroy()
        
        if not self.expenses:
            tk.Label(self.expenses_frame, text="No expenses found.", bg="#e0f7fa", font=("Helvetica", 12)).pack()
            return

        for expense in self.expenses:
            expense_text = f"${expense['amount']} - {expense['category']} ({expense['date']})\n{expense['description']}"
            tk.Label(self.expenses_frame, text=expense_text, bg="#b2dfdb", fg="black", font=("Helvetica", 10), anchor="w", padx=5, pady=5, relief="solid").pack(fill="x", pady=2)

    def analyze_expenses(self):
        summary = {}
        for expense in self.expenses:
            category = expense["category"]
            summary[category] = summary.get(category, 0) + expense["amount"]
        
        summary_text = "\n".join(f"{category}: ${total:.2f}" for category, total in summary.items())
        messagebox.showinfo("Expense Summary", summary_text or "No expenses found.")

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()