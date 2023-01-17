import sqlite3
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Create and connect to SQLite database
conn = sqlite3.connect('finance.db')
c = conn.cursor()

# Create transactions table in the database
c.execute('''CREATE TABLE IF NOT EXISTS transactions (date text, description text, amount real)''')

# Function to add a transaction
def add_transaction():
    date = date_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()

    # Validate date input
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("Incorrect date format, should be YYYY-MM-DD")
        return

    # Validate description input
    if len(description) == 0:
        print("Description cannot be empty")
        return

    # Validate amount input
    try:
        float(amount)
    except ValueError:
        print("Amount should be a number")
        return

    c.execute("INSERT INTO transactions (date, description, amount) VALUES (?, ?, ?)", (date, description, amount))
    conn.commit()
    print("Transaction added successfully")

# Function to view transactions
def view_transactions():
    c.execute("SELECT * FROM transactions")
    rows = c.fetchall()
    for row in rows:
        print(row)

# Function to generate a report
def generate_report():
    c.execute("SELECT amount FROM transactions")
    data = c.fetchall()
    data = np.array([i[0] for i in data]).astype(float)
    plt.hist(data)
    plt.show()

# Tkinter GUI code
root = Tk()

date_label = Label(root, text="Date")
date_label.grid(row=0, column=0)
date_entry = Entry(root)
date_entry.grid(row=0, column=1)

description_label = Label(root, text="Description")
description_label.grid(row=1, column=0)
description_entry = Entry(root)
description_entry.grid(row=1, column=1)

amount_label = Label(root, text="Amount")
amount_label.grid(row=2, column=0)
amount_entry = Entry(root)
amount_entry.grid(row=2, column=1)

add_button = Button(root, text="Add", command=add_transaction)
add_button.grid(row=3, column=0)

view_button = Button(root, text="View", command=view_transactions)
view_button.grid(row=3, column=1)

report_button = Button(root, text="Report", command=generate_report)
report_button.grid(row=3, column=2)

root.mainloop()