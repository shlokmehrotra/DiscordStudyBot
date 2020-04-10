import mysql.connector 
import discord
import numpy as np
import pandas as pd
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import time 
from dateutil.relativedelta import relativedelta
import schedule

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "bruhprenk", database = "toughguy")

mydb.autocommit = True
mycursor = mydb.cursor()


def time_process(time_curr, time_lat):

	time_curr = time_curr.split('.')[0]
	time_curr = datetime.strptime(time_curr, '%Y-%m-%d %H:%M:%S')
	t_diff = time_lat - time_curr

	#in minutes
	time_intervals = [1, 5, 10, 30, 60, 180, 300, 1440, 2880, 4320, 10080]
	print(t_diff)
	if(t_diff.days < 0):
		seconds = -1 * (t_diff.seconds - t_diff.days * 86400)
		print(seconds)
		for value in time_intervals:
			if(int(seconds/60) == value):
				#time that needs to be sent :)
				return value
		#time has not come up
		return 0
	else:
		#the item should be deleted
		return -1


def iterate()
	mycursor.execute("SELECT * FROM userlog")
	rows = mycursor.fetchall()
	for row in rows:
 		print(row[0] ,"this ", row[1],"this", row[2])
 		time_process(row[2], datetime.utcnow())

schedule.every(1).minutes.do(iterate)