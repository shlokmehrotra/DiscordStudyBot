import mysql.connector 
import discord
import numpy as np
import pandas as pd
from discord.ext import commands
from datetime import datetime, timedelta
import time 
from dateutil.relativedelta import relativedelta

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "bruhprenk", database = "toughguy")

mydb.autocommit = True
mycursor = mydb.cursor()


def time_process(time_curr, time_lat):
	#time_curr = datetime.now()
	#time_lat = time_curr + timedelta(days = 1, hours = 1, minutes = 3)
	t_diff = time_lat - time_curr
	#return t_diff
	print(time_curr, " future: ", time_lat)
	print(t_diff)
i = 0
while(i < 3):
		
	mycursor.execute("SELECT * FROM userlog")
	rows = mycursor.fetchall()
	for row in rows:
 		print(row[0] ,"this ", row[1],"this", row[2])
 		time_process(row[2], datetime.now())
	time.sleep(60)
	i+=1
time_process(1, 1)