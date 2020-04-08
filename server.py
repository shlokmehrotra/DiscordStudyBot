import mysql.connector 
import discord
import numpy as np
import pandas as pd
from discord.ext import commands
from datetime import datetime, timedelta
import time 
#import mysqlx


mydb = mysql.connector.connect(host = "localhost", user = "root", password = "bruhprenk", database = "toughguy")

mycursor = mydb.cursor()
'''
#for adding things to the database.
mycursor.execute("INSERT INTO userlog VALUES ",
                "( 'value1', 'value2', 'value3')")
'''
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
  return(datetime.now() + timedelta(days = int(days), hours=int(hours), minutes = int(minutes)))
  '''
  days, hours, minutes = time_from_now.split(':')
  time_left = minutes + hours * 60 + days * 60 * 24
  return time_left
  print(days, hours, minutes)
  '''
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
  #session.start_transaction()

  #session.commit()
  #prenk
  '''
  # check for duplicate tasks
  if task.lower() not in list(tasks['task']):
    tasks = tasks.append(pd.Series([ctx.author, task.lower(), time], index=tasks.columns), ignore_index=True)
    print(tasks)
    await ctx.send(f"Added {task} successfully! :rotating_light:")
  else:
    await ctx.send(f"{task} already exists. Did you want to update it? :eggplant:")
  '''
# delete items from schedule
@client.command() 
async def delete(ctx, task):
  #global tasks
  #if task.lower() in list(tasks['task']):
  # tasks = tasks.set_index("task")
  # tasks = tasks.drop(task)
  #  tasks = tasks.reset_index()
  #  await ctx.send(f"Deleted {task} successfully! :octopus:" ,  ctx.content, task.content)
  #else:
  # await ctx.send(f"{task} not found. Would you like to create it? :popcorn:" , ctx.content, task.content)
  await ctx.send("Delete")

# update items
@client.command()
async def update(ctx, task, time):
  await ctx.send("Update")
  
# show items specific to user
@client.command()
async def show(ctx):
  await ctx.send("Show")

# indicate that item is completed
@client.command()
async def complete(ctx, task):
  await ctx.send("Complete")



#dont touch the below tings
client.run("Njg5NzcwODc3OTk0NTMyODg0.XnHtRA.woz3RKnzeaztW2dTrhpbLekA68g")