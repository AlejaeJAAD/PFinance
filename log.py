import csv
import datetime

def log_email(recipient, status):
    log_file = "./csv/email_logs.csv"
    log_fields = ['Time', 'Recipient', 'Status']
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = [time, recipient, status]

    with open(log_file, 'a') as csvfile:
        writer = csv.writer(csvfile)

        if not csvfile.tell():
            writer.writerow(log_fields)

        writer.writerow(log_data)

recipient = 'alejandroanayadom@gmail.com'
log_email(recipient, "sent")

# You can also add a feature to log the email sending activities, 
# such as the time of sending, the recipient's email address, and the status of the email (sent, failed, etc.).