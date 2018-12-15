import mysql.connector
import matplotlib
import LocalLibrary as ll
import DataTransmitter as dt
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

import random
dataT = dt.DatabaseClient()
print(dataT)
cursor = dataT.getCursor()
dataT.setQuery("show databases;")
dataT.performQuery()
for x in cursor:
    print(x)
dataT.setQuery("use odendata;")
dataT.performQuery()
ll.DeleteCSVFile("test")
dataT.setQuery(ll._selectBaseData + ll._outputToFile)
dataT.performQuery()

#result=dataT.getCursor.fetchall()
#c = csv.writer(open("test.csv","wb"))
#c.writerow(result)
dataT.close()