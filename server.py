import discord
import numpy as np
import pandas as pd
from discord.ext import commands

client = commands.Bot(command_prefix = "!")
tasks = pd.DataFrame(columns = ["author", "task", "time"])

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  guilds = client.guilds
  
@client.command()
async def ping(ctx): 
  await ctx.send(f'Chong from Wuhan! {round(client.latency * 1000)}ms') 

# add items to schedule
@client.command()
async def add(ctx, task, time):
  tasks.append(pd.Series([ctx.author, task, time], index=tasks.columns))
  await ctx.send(f"Added {task} successfully!")
  

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