import mysql.connector

conn = mysql.connector.connect(user ='root', password='password', host = '127.0.0.1')
print(conn)
mycursor = conn.cursor()
mycursor.execute("show databases;")
for x in mycursor:
    print(x)
mycursor.execute("use odendata;")
mycursor.execute("SELECT * FROM odendata.`517_foam_extrusion_9-30_12-3`;")
for x in mycursor:
    print(x)

mycursor.close()
conn.close()