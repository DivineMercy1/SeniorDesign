import mysql.connector
import matplotlib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import DataTransmitter as dt
conn = mysql.connector.connect(user = dt._userName, password= dt._password, host = dt._host)
print(conn)
mycursor = conn.cursor()
mycursor.execute("show databases;")
for x in mycursor:
    print(x)
mycursor.execute("use odendata;")
mycursor.execute(
    "SELECT * FROM odendata.`517_foam_extrusion_9-30_12-3`" +
    "INTO OUTFILE 'D:/Programs/Dropbox/Senior Design/test.csv'" +
    "FIELDS TERMINATED BY ','" +
    "ENCLOSED BY '\"'" +
    "LINES TERMINATED BY '\n';")
for x in mycursor:
    print(x)

mycursor.close()
conn.close()