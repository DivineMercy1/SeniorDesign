import LocalLibrary as ll
import mysql.connector

_userName = "root"
_password = "password"
_records = []
_recipients = []
_emailData = "Forecasting summary/information:"
_emailImages = []
_databaseName = ""
_host = "127.0.0.1"
class DatabaseClient:
    def __init__(self):
        self._currentQuery = ""
        self._conn = mysql.connector.connect(user = _userName, password= _password, host = _host)
        self._mycursor = self._conn.cursor()

    # sets the query to the desired string to perform
    def setQuery(self, newQ):
        self._currentQuery = newQ
        return

    def getQuery(self):
        return self._currentQuery

    # performs the current query
    def performQuery(self):
        # execute query
        self._mycursor.execute(self._currentQuery)
        return

    #returns the cursor
    def getCursor(self):
        return self._mycursor
    #returns the cursor - prepared
    def getPreparedCursor(self):
        return self._conn.cursor(prepared = True)

    def close(self):
        self._mycursor.close()
        self._conn.close()
        return
    def comm(self):
        self._conn.commit()
# ---------------- Send email portion of transmitter -------------
def SendEmails():
    import smtplib
    import os
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # credentials
    fromEmail = "rfsworldnotif"
    fromPass = "rfstest1"
    # who receives email
    recipients = _recipients
    # login
    server.login(fromEmail, fromPass)
    # set message details
    msg = MIMEMultipart()
    text = MIMEText(_emailData)
    global _emailImages
    for img in _emailImages:
        img_data = open(img, 'rb').read()
        msg.attach(MIMEImage(img_data, name=os.path.basename(img)))
    _emailImages = []
    msg.attach(text)
    msg['Subject'] = "Test - SD"
    msg['From'] = fromEmail
    msg['To'] = ", ".join(recipients)
    #send email
    server.sendmail(fromEmail, recipients, msg.as_string())
    server.quit()

def AddEmailText(strToAdd):
    global _emailData
    _emailData = _emailData + "\n" + strToAdd

def AddEmailImage(imgName):
    global _emailImages
    _emailImages.append(imgName)

def AddEmailRecipients(arr):
    global _recipients
    for em in arr:
        _recipients.append(em)