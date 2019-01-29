import os
ROOT = os.path.abspath("").replace('\\', '/')
_selectBaseData = "SELECT * FROM odendata.massdata "
_selectMotorRpmTrain = "(SELECT * FROM odendata.motorrpmpullout order by timestamp asc) "
_selectColumnHeaders = "Select \"values\", \"timestamp\" union all "
#_outputToFile = "INTO OUTFILE '" + ROOT + "/test.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n';"
def OutputToFileNameQuery(fileName):
    _outputToFile = "INTO OUTFILE '" + ROOT + "/" + fileName + ".csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n';"
    return _outputToFile
def DeleteCSVFile(f):
    f = f + ".csv"
    if os.path.exists(f):
        os.remove(f)
    return
