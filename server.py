import mysql.connector 
import discord
import numpy as np
import pandas as pd
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import time 

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "bruhprenk", database = "toughguy")

mydb.autocommit = True
mycursor = mydb.cursor()

mycursor.execute("select * from userlog")
for prenk in mycursor:
  print(prenk)

client = commands.Bot(command_prefix = "!")


tasks = pd.DataFrame(columns = ["author", "task", "time"]) 

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  guilds = client.guilds
  
@client.command()
async def ping(ctx): 
  await ctx.send(f'pong! {round(client.latency * 1000)}ms') 

# time format DD:HH:MM
# add items to schedule
# time_fromnow takes up DD:HH:MM format

def time_process(time_from_now):
  time_from_now = time_from_now.split(':')
  days = 0
  if(len(time_from_now) == 2):
    hours, minutes =  time_from_now[0], time_from_now[1]
  if(len(time_from_now) == 3):
    days, hours, minutes = time_from_now[0], time_from_now[1], time_from_now[2]
  return(datetime.now(timezone.utc) + timedelta(days = int(days), hours=int(hours), minutes = int(minutes)))

@client.command()
async def add(ctx, task, time):
  #global tasks 

  print(ctx.author.id) #author id
  print(task, time)


  #process the time to calculate end date
  time = time_process(time)
  #adding item to database
  comm = (
  "INSERT INTO userlog (user, item, endtime) VALUES (%s, %s, %s)"
  )
  data = (str(ctx.author.id), str(task), str(time))
  mycursor.execute(comm, data)
  mycursor.execute("SELECT * FROM userlog")
  rows = mycursor.fetchall()
  print(rows)

# delete items from schedule
@client.command() 
async def delete(ctx, task):
  data = (str(ctx.author.id), str(task))
  comm = (
  "DELETE FROM userlog WHERE user = %s  AND item = %s" 
  )

  mycursor.execute(comm, data)

  await ctx.send("Deleted task: %s" % task)

# update items
@client.command()
async def update(ctx, task, new_time):
  comm = ("SELECT * FROM userlog WHERE user = %d")
  data = (ctx.author.id)
  mycursor.execute(comm  % data)
  rows = mycursor.fetchall()
  print("user vals: ")
  condition = True
  for row in rows:
    if(row[1] == str(task)):
      condition = False
    print(row[1])
  if(condition):
    await ctx.send("You do not have a task by that name. Please try again!")
  else:
    comm = ("UPDATE userlog SET endtime = %s WHERE (item = %s AND user = %s)")
    new_time = time_process(new_time)
    data = (new_time, task, ctx.author.id)
    mycursor.execute(comm, data)
    await ctx.send("You have updated you task: " + str(task))
# show items specific to user
@client.command()
async def show(ctx):
  comm = (
  "SELECT * FROM userlog WHERE user = %d"
  )
  data = (ctx.author.id)
  print(ctx.author.id)
  mycursor.execute(comm % (data))
  rows = mycursor.fetchall()
  print(rows)
  if(len(rows) == 0):
    await ctx.send("Currently, you have no items. Please add items to view your current itemlist")
  else:
    for row in rows:  
      await ctx.send(str(row))
  #await ctx.send("Show")

# indicate that item is completed
@client.command()
async def complete(ctx, task):
  data = (str(ctx.author.id), str(task))
  comm = (
  "DELETE FROM userlog WHERE user = %s  AND item = %s" 
  )
  
  mycursor.execute(comm, data)
  await ctx.send("Congrats you completed: %s successfully" % task)


#dont touch the below tings
client.run("Njg5NzcwODc3OTk0NTMyODg0.XnHtRA.woz3RKnzeaztW2dTrhpbLekA68g")