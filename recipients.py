import pandas as pd
import csv

# def import_recipients(file_path):
#         recipients = []
#         with open(file_path, 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             for row in reader:
#                 recipients.append(row[0])
#         return recipients

def import_recipients(file_path):
    recipients_df = pd.read_csv(file_path)
    recipients = recipients_df["email"].tolist()
    return recipients


recipients = import_recipients("./csv/recipients.csv")
print(recipients)

# You can add a feature to import a list of recipients from a CSV file or a spreadsheet,
# so you don't have to manually enter them every time you need to send an email.