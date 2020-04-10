import mysql.connector 
import discord
import numpy as np
import pandas as pd
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import time 
from dateutil.relativedelta import relativedelta

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "bruhprenk", database = "toughguy")

mydb.autocommit = True
mycursor = mydb.cursor()


def time_process(time_curr, time_lat):
	#time_curr = datetime.now()
	#time_lat = time_curr + timedelta(days = 1, hours = 1, minutes = 3)
	time_curr = time_curr.split('.')[0]
	time_curr = datetime.strptime(time_curr, '%Y-%m-%d %H:%M:%S')
	t_diff = time_lat - time_curr
	#return t_diff
	#print(time_curr, " future: ", time_lat)
	print(t_diff)
	#print(t_diff.days)
	#print(t_diff.seconds)
	if(t_diff.days < 0):
		seconds =  -(t_diff.days * 216000 + t_diff.seconds)
		days = int(seconds / 216000)
		seconds -= 216000 * days
		hours = int(seconds / 3600)
		seconds -= hours * 3600
		minutes = seconds / 60
		seconds -= minutes * 60
		print(seconds, minutes, hours, days)

i = 0
while(i < 3):
		
	mycursor.execute("SELECT * FROM userlog")
	rows = mycursor.fetchall()
	for row in rows:
 		print(row[0] ,"this ", row[1],"this", row[2])
 		time_process(row[2], datetime.now(timezone.utc))
	time.sleep(60)
	i+=1
time_process(1, 1)