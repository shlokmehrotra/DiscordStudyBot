import discord
import numpy as np
import pandas as pd
from discord.ext import commands
import time

client = commands.Bot(command_prefix = "!")
tasks = pd.DataFrame(columns = ["author", "task", "time"])

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  guilds = client.guilds

@client.command()
async def ping(ctx):
  await ctx.send(f'Chong from Wuhan! {round(client.latency * 1000)}ms')

# time format DD:HH:MM
# add items to schedule
# time_fromnow takes up DD:HH:MM format
def time_waste(time_from_now):
  print(time.ctime())

@client.command()
async def add(ctx, task, time):
  global tasks
  # check for duplicate tasks
  if task not in list(tasks['task']):
    tasks = tasks.append(pd.Series([ctx.author, task, time], index=tasks.columns), ignore_index=True)
    print(tasks)
    await ctx.send(f"Added {task} successfully! :rotating_light:")
  else:
    await ctx.send(f"{task} already exists. Did you want to update it? :eggplant:")

# delete items from schedule
@client.command()
async def delete(ctx, task):
  await ctx.send("Delete" ,  ctx.content, task.content)

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
