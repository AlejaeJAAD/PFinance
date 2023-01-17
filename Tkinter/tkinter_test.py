import sqlite3
import tkinter as tk
import csv
import os
from tkinter import StringVar, filedialog
from tkinter import messagebox
import mysql.connector

def backup_restore_window():
    # Create a new tkinter window
    window = tk.Tk()
    window.title("Backup/Restore")

    # Create checkboxes for each table
    table_var1 = tk.IntVar()
    table1_checkbox = tk.Checkbutton(window, text="Table 1", variable=table_var1)
    table1_checkbox.pack()

    table_var2 = tk.IntVar()
    table2_checkbox = tk.Checkbutton(window, text="Table 2", variable=table_var2)
    table2_checkbox.pack()

    table_var3 = tk.IntVar()
    table3_checkbox = tk.Checkbutton(window, text="Table 3", variable=table_var3)
    table3_checkbox.pack()

    # Create a backup button
    backup_button = tk.Button(window, text="Backup", command=lambda: backup())
    backup_button.pack()

    # Create a restore button
    restore_button = tk.Button(window, text="Restore", command=lambda: restore(table_var1, table_var2, table_var3))
    restore_button.pack()

    window.mainloop()

# def backup(table_list):
#     # Get the file name and location to save the backup file
#     file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV file", "*.csv")])
#     if file_name:
#         with open(file_name, "w", newline="") as f:
#             writer = csv.writer(f)
#             for table in table_list:
#                 # Retrieve the data from the selected table in the database
#                 data = retrieve_data_from_db(table)
#                 # Write the data to the CSV file
#                 writer.writerows(data)
#                 # Popup message to show the success of backup
#                 messagebox.showinfo("Success", f"{table} Data backed up successfully to {file_name}")

def backup():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if not file_path:
        return

    table_var1 = StringVar(value="income")
    table_var2 = StringVar(value="expenses")
    table_var3 = StringVar(value="transactions")
    table_var4 = StringVar(value="budget")
    table_var5 = StringVar(value="goals")

    selected_tables = []
    if table_var1.get() == "1":
        selected_tables.append("income")
    if table_var2.get() == "1":
        selected_tables.append("expenses")
    if table_var3.get() == "1":
        selected_tables.append("transactions")
    if table_var4.get() == "1":
        selected_tables.append("budget")
    if table_var5.get() == "1":
        selected_tables.append("goals")

    # Code to connect to the database and retrieve the data for the selected tables
    # ...
    for table in selected_tables:
        data = retrieve_data_from_db(table)
        with open(file_path, mode='w') as csv_file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    print("Data successfully exported to: ", file_path)

def restore(table_list):
    # Get the file name and location of the backup file
    file_name = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV file", "*.csv")])
    if file_name:
        with open(file_name, "r") as f:
            reader = csv.reader(f)
            for table in table_list:
                data = []
                # Retrieve the data from the selected table in the CSV file
                for row in reader:
                    data.append(row)
                # Insert the data into the corresponding table in the database
                insert_data_to_db(table, data)
                # Popup message to show the success of restore
                messagebox.showinfo("Success", f"{table} Data restored successfully from {file_name}")

def restore():
    # code to open a file dialog and let the user select the csv file
    file_path = filedialog.askopenfilename()
    table_list = []
    if table_var1.get() == 1:
        table_list.append("income")
    if table_var2.get() == 1:
        table_list.append("expenses")
    if table_var3.get() == 1:
        table_list.append("transactions")
    if table_var4.get() == 1:
        table_list.append("budget")
    if table_var5.get() == 1:
        table_list.append("goals")
    if table_var6.get() == 1:
        table_list.append("progress")
    if table_var7.get() == 1:
        table_list.append("recurring_transactions")
    if table_var8.get() == 1:
        table_list.append("reminders")
    if not table_list:
        messagebox.showerror("Error", "Please select at least one table to restore.")
        return
    execute_restore(file_path, table_list)

def execute_restore(file_path, table_list):
    # code to connect to the database
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()
    # code to read the csv file
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for table in table_list:
            cursor.execute("DELETE FROM {}".format(table))
            for row in csv_reader:
                if row[0] == table:
                    # code to insert the data into the corresponding table in the database
                    cursor.execute("INSERT INTO {} VALUES {}".format(table, tuple(row[1:])))
    conn.commit()
    messagebox.showinfo("Success", "Data has been successfully restored.")

def insert_data_to_db(table_name, data):
    # Connect to the database
    connection = sqlite3.connect("finance_manager.db")
    cursor = connection.cursor()

    # Loop through the data and insert it into the specified table
    for item in data:
        keys = ', '.join(item.keys())
        values = ', '.join(['?' for i in range(len(item.keys()))])
        cursor.execute(f'INSERT INTO {table_name} ({keys}) VALUES ({values})', tuple(item.values()))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

def retrieve_data_from_db(table_name):
    # Connect to the database
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="root1324",
    #     database="your_database"
    # )

    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Create a cursor object
    # cursor = mydb.cursor()

    # Execute the SELECT statement
    print('dkflfl')
    print(table_name, 'fgfg')
    cursor.execute(f"SELECT * FROM {table_name}")

    # Fetch all the rows
    rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    # mydb.close()

    return rows

backup_restore_window()