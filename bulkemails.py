import csv

def send_bulk_emails(sender_email, sender_password, subject, message_template, csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipient_email = row['email']
            message = message_template.format(**row)
            send_email(sender_email, sender_password, recipient_email, subject, message)

csv_file = "./csv/recipients.csv"
message_template = "Hello {name},\nThank you for your interest in our product.\nBest Regards,\nYour Company"
send_bulk_emails(sender_email, sender_password, subject, message_template, csv_file)