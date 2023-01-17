from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_attachment(sender_email, sender_password, recipient_emails, subject, message, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    with open(attachment_path, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())

    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", f"attachment; filename={attachment_path}")
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_emails, msg.as_string())
    server.quit()


attachment_path = "./pdf/attachment.pdf"
send_email_with_attachment(sender_email, sender_password, recipients, subject, message, attachment_path)

# You can also add a feature to attach files to the email, such as images or documents.