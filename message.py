import mysql.connector 
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import time 
from dateutil.relativedelta import relativedelta
import schedule

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "bruhprenk", database = "toughguy")

mydb.autocommit = True
mycursor = mydb.cursor()

client = commands.Bot(command_prefix = "!")
'''
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
	#the item should be deleted ting
	return -1


def iterate():
	mycursor.execute("SELECT * FROM userlog")
	rows = mycursor.fetchall()
	for row in rows:
		#row[0] = user id
		#row[1] = task
		#row[2] = time
 		print(row[0] ,"this ", row[1],"this", row[2])
 		action = time_process(row[2], datetime.utcnow())
 		if(action == 0):
 			pass
 		elif(action == -1):
 			data = (str(row[0]), str(row[1]))
 			comm = (
  			"DELETE FROM userlog WHERE user = %s  AND item = %s"
  			)
  			mycursor.execute(comm, data)
  		else:
 			#PM the USER with the deadline update
 			client.get_user(str(row[0])).send("Hey, you have " + str(action) + " minutes left to complete you task. Stay on schedule!")
#schedule.every(1).minutes.do(iterate)
'''


def timeDifferential(time_curr, time_lat):
  time_lat = time_lat.split('.')[0]
  time_lat = datetime.strptime(time_lat, '%Y-%m-%d %H:%M:%S')
  t_diff = time_lat - time_curr
  seconds = -1 * (t_diff.seconds + t_diff.days * 86400)
  minutes = int(seconds / 60)
  days = int(minutes / 1440)
  minutes = minutes -  days * 1440
  hours = int(minutes / 60)
  minutes = minutes - hours * 60
  return(days, hours, minutes)

user = client.get_user(430610739389267968)
user.send("hi")

client.run("Njg5NzcwODc3OTk0NTMyODg0.XnHtRA.woz3RKnzeaztW2dTrhpbLekA68g")
