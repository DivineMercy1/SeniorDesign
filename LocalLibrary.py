import os
ROOT = os.path.abspath("").replace('\\', '/')
_selectBaseData = "SELECT * FROM odendata.`517_foam_extrusion_9-30_12-3` WHERE (`Barrel Pressure Before Gas - Pressures` AND `Capacitance - Cold (pF/ft) - Main Measurement` AND `Line Speed (fpm) - Main Measurement` AND `Adapter (°F) - Co-Poly Temperatures`) <> 0 "
_outputToFile = "INTO OUTFILE '" + ROOT + "//test.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n';"
def ConstructSpecificQuery(qToModify, q):
    qModified = qToModify
    return qModified
def DeleteCSVFile(f):
    f = f + ".csv"
    if os.path.exists(f):
        os.remove(f)
    return
