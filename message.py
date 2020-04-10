import mysql.connector 
import discord
import numpy as np
import pandas as pd
from discord.ext import commands
from datetime import datetime, timedelta
import time 

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "bruhprenk", database = "toughguy")

mydb.autocommit = True
mycursor = mydb.cursor()



client = commands.Bot(command_prefix = "!")
time_intervals = [1, 5, 10, 30, 60]

while(True):
	mycursor.execute("SELECT * FROM userlog")
	rows = mycursor.fetchall()
	for row in rows:
 		print(row[0] ,"this ", row[1],"this", row[2])
	time.sleep(60)