import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP server setup
smtp_host = "smtp.office365.com"
smtp_port = 587
smtp_user = "xxxxxxxxxxxxx"
smtp_password = "xxxxxxxxxxxxx"

# Email body
email_body = "Your email body goes here"

# Send email
msg = MIMEMultipart('alternative')
msg['Subject'] = 'Your subject'
msg['From'] = smtp_user
msg['To'] = 'xxxxxxxxxxxxxxxxxx'  # Replace with the recipient's email address
part1 = MIMEText(email_body, 'plain')
msg.attach(part1)

s = smtplib.SMTP(host=smtp_host, port=smtp_port)
s.starttls()
s.login(smtp_user, smtp_password)
s.send_message(msg)
s.quit()

