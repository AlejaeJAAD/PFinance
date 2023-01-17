from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email_with_tracking(sender_email, sender_password, recipient_emails, subject, message, tracking_url):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    # open the tracking pixel and attach it to the email
    with open("tracking_pixel.gif", "rb") as f:
        img_data = f.read()
    image = MIMEImage(img_data, name="tracking_pixel.gif")
    image.add_header('Content-ID', '<tracking_pixel>')
    msg.attach(image)

    # replace the URL of the tracking pixel with the actual tracking URL
    message = message.replace("http://example.com/tracking_pixel.gif", tracking_url)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_emails, msg.as_string())
    server.quit()

sender_email = "example@gmail.com"
sender_password = "password"
recipient_email = "recipient@example.com"
subject = "Hello"
message = "This is a test email with tracking pixel"
tracking_url = "https://example.com/track"

send_email_with_tracking(sender_email, sender_password, recipient_email, subject, message, tracking_url)


# Email tracking pixels: You can include a small image,
# called a tracking pixel, in your email. When the email is opened,
# the tracking pixel will be downloaded from a server,
# which you can track to determine if the email has been opened.