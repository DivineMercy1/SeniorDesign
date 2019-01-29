import LocalLibrary as ll
import mysql.connector

_userName = "root"
_password = "password"
_records = []
_emailData = []
_databaseName = ""
_host = "127.0.0.1"
class DatabaseClient:
    def __init__(self):
        self._currentQuery = ""
        self._conn = mysql.connector.connect(user = _userName, password= _password, host = _host)
        self._mycursor = self._conn.cursor()
    # retrieve data in csv format
    def getData(self):
        # perform query
        # save as csv in the current working folder
        return

    #after retrieving the data, cleanse poor values
    def cleanData(self):
        # find any outliers and remove them from the dataset
        # store this to the dataset
        # push clean data set used to the server
        return

    # returns the clean data set
    def getCleanData(self):
        # return the clean data
        return

    # sets the query to the desired string to perform
    def setQuery(self, newQ):
        self._currentQuery = newQ
        return

    # performs the current query
    def performQuery(self):
        # execute query
        self._mycursor.execute(self._currentQuery)
        return
    # sends emails to the selected addresses.
    def sendEmails(self):
        return

    #returns the cursor
    def getCursor(self):
        return self._mycursor

    def close(self):
        self._mycursor.close()
        self._conn.close()
        return
