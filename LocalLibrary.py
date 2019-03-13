import os, shutil
ROOT = os.path.abspath("").replace('\\', '/')
_selectBaseData = "SELECT * FROM odendata.massdata "
_selectColumnHeaders = "Select \"values\", \"timestamp\" union all "
#_outputToFile = "INTO OUTFILE '" + ROOT + "/test.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n';"
def OutputToFileNameQuery(fileName):
    _outputToFile = "INTO OUTFILE '" + ROOT + "/dump/" + fileName + ".csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n';"
    return _outputToFile

def DeleteCSVFile(f):
    f = "dump/" + f + ".csv"
    if os.path.exists(f):
        os.remove(f)
    return

def SelectMetric(metricName):
    return "(SELECT * FROM odendata." + metricName + " order by timestamp asc) "

def GetMetrics():
    return "SELECT metricName FROM criticalmetrics;"

def InsertForecast():
    q = "INSERT INTO odendata.forecasteddata (predictedValue, predictedDate, predictedLowerValue, predictedUpperValue, metricName) VALUES ( %s, %s, %s, %s, %s);"
    return q
def ClearForecast():
    q = "TRUNCATE TABLE odendata.forecasteddata;"
    return q
def GetEmails():
    q = "SELECT email from odendata.emails;"
    return q
# deletes the images stored in the folder path given
def DeleteImageFolder(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)