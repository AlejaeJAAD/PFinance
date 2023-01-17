import smtplib
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class EmailSender(QWidget):
    def __init__(self):
        super().__init__()

        self.sender_email = QLineEdit()
        self.sender_password = QLineEdit()
        self.recipient_emails = QLineEdit()
        self.subject = QLineEdit()
        self.message = QLineEdit()

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_email)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Sender Email:"))
        layout.addWidget(self.sender_email)
        layout.addWidget(QLabel("Sender Password:"))
        layout.addWidget(self.sender_password)
        layout.addWidget(QLabel("Recipient Emails (comma separated):"))
        layout.addWidget(self.recipient_emails)
        layout.addWidget(QLabel("Subject:"))
        layout.addWidget(self.subject)
        layout.addWidget(QLabel("Message:"))
        layout.addWidget(self.message)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_email(self):
        sender_email = self.sender_email.text()
        sender_password = self.sender_password.text()
        recipient_emails = self.recipient_emails.text().split(",")
        subject = self.subject.text()
        message = self.message.text()

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = ", ".join(recipient_emails)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_emails, msg.as_string())
        server.quit()

if __name__ == '__main__':
    app = QApplication([])
    email_sender = EmailSender()
    email_sender.show()
    app.exec_()
    # recipients = app.import_recipients("recipients.csv")
