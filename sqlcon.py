import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "bruhprenk", database = "toughguy")

mycursor = mydb.cursor()

mycursor.execute("INSERT INTO userlog VALUES ( 'value1', 'value2', 'value3')")
mycursor.execute("select * from userlog")
for prenk in mycursor:
	print(prenk)