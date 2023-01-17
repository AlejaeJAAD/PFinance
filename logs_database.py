import sqlite3
import datetime

def log_email(recipient, status):
    conn = sqlite3.connect('email_logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS email_logs
                (time text, recipient text, status text)''')
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = (time, recipient, status)
    c.execute("INSERT INTO email_logs VALUES (?,?,?)", log_data)
    conn.commit()
    conn.close()

recipient = 'alejandroanayadom@gmail.com'
log_email(recipient, "sent")

# You can also modify the function to write the logs to a database or to a text file, depending on your preference.