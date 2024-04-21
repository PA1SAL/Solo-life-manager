import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x400")  # Larger window size

        # Initialize database connection
        self.conn = sqlite3.connect('expenses.db')
        self.cursor = self.conn.cursor()

        # Create expenses table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            amount REAL,
                            description TEXT,
                            date DATE)''')
        self.conn.commit()

        # Background image
        self.bg_image = Image.open("exp.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create GUI elements
        self.label = tk.Label(root, text="Expense Tracker", font=("Arial", 24), bg="white")
        self.label.pack(pady=20)

        self.amount_label = tk.Label(root, text="Enter Expense:", bg="white")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()

        self.description_label = tk.Label(root, text="Enter Description:", bg="white")
        self.description_label.pack()

        self.description_entry = tk.Entry(root)
        self.description_entry.pack()

        self.date_label = tk.Label(root, text="Enter Date (YYYY-MM-DD):", bg="white")
        self.date_label.pack()

        self.date_entry = tk.Entry(root)
        self.date_entry.pack()

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Reset Database", command=self.reset_database)
        self.reset_button.pack(pady=5)

        self.show_button = tk.Button(root, text="Show Expenses", command=self.show_expenses)
        self.show_button.pack(pady=5)

        self.plot_button = tk.Button(root, text="Plot Expenses", command=self.plot_expenses)
        self.plot_button.pack(pady=5)

    def add_expense(self):
        amount = self.amount_entry.get()
        description = self.description_entry.get()
        date_str = self.date_entry.get()
        if amount and date_str:
            try:
                amount = float(amount)
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                self.cursor.execute("INSERT INTO expenses (amount, description, date) VALUES (?, ?, ?)", (amount, description, date))
                self.conn.commit()
                self.amount_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)
                self.date_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a valid amount and date (YYYY-MM-DD).")

    def reset_database(self):
        confirm_reset = messagebox.askyesno("Reset Database", "Are you sure you want to reset the database? This will delete all expenses.")
        if confirm_reset:
            self.cursor.execute("DROP TABLE IF EXISTS expenses")
            self.cursor.execute('''CREATE TABLE expenses
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                amount REAL,
                                description TEXT,
                                date DATE)''')
            self.conn.commit()
            messagebox.showinfo("Reset Database", "Database has been reset successfully.")

    def show_expenses(self):
        self.cursor.execute("SELECT amount, description, date FROM expenses ORDER BY date")
        expenses = self.cursor.fetchall()
        if expenses:
            show_window = tk.Toplevel(self.root)
            show_window.title("Show Expenses")
            show_window.geometry("500x300")
            show_text = scrolledtext.ScrolledText(show_window, wrap=tk.WORD, width=50, height=15)
            show_text.pack(expand=True, fill='both')
            show_text.insert(tk.END, "Date\t\tAmount\tDescription\n")
            for expense in expenses:
                show_text.insert(tk.END, f"{expense[2]}\t${expense[0]}\t{expense[1]}\n")
            show_text.configure(state='disabled')
        else:
            messagebox.showinfo("Show Expenses", "No expenses recorded.")

    def plot_expenses(self):
        self.cursor.execute("SELECT description, SUM(amount) FROM expenses GROUP BY description")
        expenses = self.cursor.fetchall()
        if expenses:
            descriptions = [expense[0] for expense in expenses]
            amounts = [float(expense[1]) for expense in expenses]
            plt.pie(amounts, labels=descriptions, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title('Expense Breakdown')
            plt.show()
        else:
            messagebox.showwarning("No Expenses", "No expenses to plot.")

def main():
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
