import tkinter as tk
from tkinter import messagebox, StringVar, filedialog
import csv
import sqlite3
import os
import pyAesCrypt

def backup():
    # Create a tkinter window
    root = tk.Tk()
    root.title("Backup")

    # Create a variable to store the selected table
    selected_table = tk.StringVar()

    # Create a function to handle the selection of the table
    def select_table():
        selected_table.set(table_var.get())

    encrypt_var = tk.BooleanVar()
    encrypt_checkbox = tk.Checkbutton(root, text="Encrypt backup file?", variable=encrypt_var)
    encrypt_checkbox.pack()

    # Create a dropdown menu to select the table
    table_var = tk.StringVar(root)
    table_var.set("Select Table") # default value
    table_dropdown = tk.OptionMenu(root, table_var, "Income", "Expenses", "Transactions", "Budget", "Goals", "Progress", "Recurring_Transactions")
    table_dropdown.pack()

    # Create a button to confirm the selection
    select_button = tk.Button(root, text="Select", command=select_table)
    select_button.pack()

    # Create a button to export the data to a CSV file
    export_button = tk.Button(root, text="Export", command=lambda: export_data_to_csv(selected_table.get(), encrypt_var.get()))
    export_button.pack()

    # Run the tkinter window
    root.mainloop()

def export_data_to_csv(table, encrypt_var):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if not file_path:
        return

    # Connect to the database and retrieve the data
    column_names, data = retrieve_data_from_db(table)
    print(column_names, data)
    # Open a file with the name of the table
    with open(file_path, "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(column_names)
        csv_writer.writerows(data)
        
    # Encrypt the backup file if the user selected the option
    buffer_size = 64 * 1024
    password = "your_password"
    print(encrypt_var)
    if encrypt_var == True:
        pyAesCrypt.encryptFile(file_path, file_path + ".aes", password, buffer_size)
        os.remove(file_path)

    messagebox.showinfo("Data successfully exported to: ", file_path)

def retrieve_data_from_db(table_name):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format(table_name))
    
    column_names = [i[0] for i in c.description]
    data = c.fetchall()
    conn.close()

    return column_names, data

#_----------------------------------------------------------_#

def restore():
    # Create tkinter window to select table and file
    root = tk.Tk()
    root.title("Restore Data")

    decrypt_var = tk.BooleanVar()
    decrypt_checkbox = tk.Checkbutton(root, text="Decrypt backup file?", variable=decrypt_var)
    decrypt_checkbox.pack()
    
    # Create tkinter variables to store table and file selections
    table_var = tk.StringVar()
    file_path = tk.StringVar()
    
    # Create tkinter label and dropdown to select table
    tk.Label(root, text="Select table:").pack()
    table_dropdown = tk.OptionMenu(root, table_var, "financial_targets", "income", "expenses", "budget", "goals", "progress", "recurring_transactions", "transactions")
    table_dropdown.pack()
    
    # Create tkinter button to select file
    #tk.Button(root, text="Select file", command=lambda: file_path.set(filedialog.askopenfilename())).pack()
    
    # Create tkinter label to display file path
    tk.Label(root, textvariable=file_path).pack()
    
    # Create tkinter button to execute restore
    tk.Button(root, text="Restore", command=lambda: execute_restore(table_var.get(), decrypt_var.get(), file_path.get())).pack()
    
    root.mainloop()

def execute_restore(table, decrypt_var, file_path):
    file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv"), ("Encrypted files", "*.aes")])
    if not file_path:
        return

    buffer_size = 64 * 1024
    password = "your_password"
    if decrypt_var == True:
        pyAesCrypt.decryptFile(file_path, file_path[:-4], password, buffer_size)
        file_path = file_path[:-4]

    # Open the CSV file and read the data
    with open(file_path, 'r') as file:
        data = csv.reader(file)
        # Insert the data into the selected table in the database
        print(table)
        insert_data_to_db(table, data)
        messagebox.showinfo("Success", f"Data imported successfully from {table}")

def insert_data_to_db(table, data):
    # Code to connect to the database
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    # Iterate through the data and insert it into the selected table
    next(data)
    for row in data:
        # cursor.execute(f"INSERT INTO {table} VALUES {tuple(row)}")
        cursor.execute(f"INSERT OR IGNORE INTO {table} VALUES (?, ?, ?)", row)
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# backup()
# restore()

import sqlite3
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('finance.db')
c = conn.cursor()

def add_transaction():
    description = description_entry.get()
    amount = amount_entry.get()
    c.execute("INSERT INTO transactions (description, amount) VALUES (?, ?)", (description, amount))
    conn.commit()

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

description_label = Label(root, text="Description")
description_label.grid(row=0, column=0)
description_entry = Entry(root)
description_entry.grid(row=0, column=1)

amount_label = Label(root, text="Amount")
amount_label.grid(row=1, column=0)
amount_entry = Entry(root)
amount_entry.grid(row=1, column=1)

add_button = Button(root, text="Add", command=add_transaction)
add_button.grid(row=3, column=0)

view_button = Button(root, text="View", command=view_transactions)
view_button.grid(row=3, column=1)

report_button = Button(root, text="Report", command=generate_report)
report_button.grid(row=3, column=2)

root.mainloop()