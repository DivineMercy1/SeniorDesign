import LocalLibrary
import mysql.connector

_userName = "root"
_password = "password"
_records = []
_currentQuery = ""
_emailData = []
_databaseName = ""
_host = "127.0.0.1"

# retrieve data in csv format
def getData():
    # perform query
    # save as csv in the current working folder
    return

#after retrieving the data, cleanse poor values
def cleanData():
    # find any outliers and remove them from the dataset
    # store this to the dataset
    # push clean data set used to the server
    return

# returns the clean data set
def getCleanData():
    # return the clean data
    return

# sets the query to the desired string to perform
def setQuery(newQ):
    _currentQuery = newQ
    return

# performs the current query set
def performQuery():
    # execute query, return the cursor
    return
# sends emails to the selected addresses.
def sendEmails():
    return
