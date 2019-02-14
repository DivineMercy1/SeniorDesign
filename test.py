import smtplib
from email.mime.text import MIMEText
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

# credentials
fromEmail = "rfsworldnotif"
fromPass = "rfstest1"
# who receives email
recipients = ["michael.marandino_jr@uconn.edu", "kyle.barry@uconn.edu", "nathan.hom@uconn.edu", "jonathan.simonin@uconn.edu"]
# login
server.login(fromEmail, fromPass)
# set message details
msg = MIMEText("""This is a test for verification that email sent through python works. Text only.""")
msg['Subject'] = "Test - SD"
msg['From'] = fromEmail
msg['To'] = ", ".join(recipients)
#send email
server.sendmail(fromEmail, recipients, msg.as_string())
server.quit()