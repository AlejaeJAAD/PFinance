import schedule
import time
import datetime

def send_emails():
    # code to send emails
    schedule.every().day.at("8:00").do(send_emails)

while True:
    now = datetime.datetime.now()
    if now.hour == 8 and now.minute == 0:
        # code to send emails
        time.sleep(60) # wait for 1 minute

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# You can also add a feature to schedule the script to run at a specific time,
# so that you can send emails automatically at a certain time every day or week.