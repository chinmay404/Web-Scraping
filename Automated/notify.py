import smtplib
from email.message import EmailMessage

def send_email(subject, message, to_address):
    from_address = "your_email@example.com"
    smtp_server = "smtp.example.com"
    smtp_port = 587
    smtp_username = "your_username"
    smtp_password = "your_password"

    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = from_address
    email["To"] = to_address
    email.set_content(message)
 
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(email)
