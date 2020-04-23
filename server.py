import mysql.connector
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import time
import asyncio
import csv

#############
# STUDY BOT #
#############

# loading credentials
with open("config.txt", "r") as f:
    credentials = []
    for line in f:
        credentials.append(line.strip())

# connecting to database
mydb = mysql.connector.connect(host=f"{credentials[0]}", user=f"{credentials[1]}",
password=f"{credentials[2]}", database=f"{credentials[3]}")

mydb.autocommit = True
mycursor = mydb.cursor()

mycursor.execute("select * from userlog")
for prenk in mycursor:
  print(prenk)

async def prenk():
  while(True):
    await iterate()
    await asyncio.sleep(60)

client = commands.Bot(command_prefix = "$")
client.remove_command("help")

async def time_process1(time_curr, time_lat):

  time_curr = time_curr.split('.')[0]
  time_curr = datetime.strptime(time_curr, '%Y-%m-%d %H:%M:%S')
  t_diff = time_lat - time_curr

  # in minutes
  time_intervals = [1, 5, 10, 30, 60, 180, 300, 1440, 2880, 4320, 10080]
  print(t_diff)
  if(t_diff.days < 0):
    seconds = -1 * (t_diff.seconds + t_diff.days * 86400)
    print("current time interval thing: ", seconds/60)
    for value in time_intervals:
      if(int(seconds/60) == value):
        # time that needs to be sent :)
        return value
    # time has not come up
    return 0
  # the item should be deleted ting
  return -1

# look for the prenks
async def iterate():
  #await asyncio.sleep(45)
  print("-----------------------------------------------------")
  mycursor.execute("SELECT * FROM userlog")
  rows = mycursor.fetchall()
  for row in rows:
    # row[0] = user id
    # row[1] = task
    # row[2] = time
    print(row[0] ,"this ", row[1],"this", row[2])
    action = await time_process1(row[2], datetime.utcnow())
    if(action == 0):
      pass
      #print("nothing new")
    elif(action == -1):
      data = (str(row[0]), str(row[1]))
      comm = (
      "DELETE FROM userlog WHERE user = %s  AND item = %s"
      )
      user = client.get_user(int(row[0]))
      await user.send(f"You should have completed your task:  **{str(row[1])}** by now.")
      mycursor.execute(comm, data)
      print("DELETED item")
    else:
      #PM the USER with the deadline update
      user = client.get_user(int(row[0]))
      await user.send(f"Hi, Please keep in mind you have **{str(action)} minutes** to complete your task: **{row[1]}**.")
      #client.get_user(int(row[0])).dm_channel("Hey, you have " + str(action) + " minutes left to complete you task. Stay on schedule!")
      print("PM complete")

    # print("script ran but nothing happened. what the shit yo. action = " + str(action))

# entering
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  guilds = client.guilds
  #await prenk()
  await prenk()

# ping thing
@client.command()
async def ping(ctx):
  await ctx.send(f'pong! **{round(client.latency * 1000)}ms**.')

# time format DD:HH:MM
# add items to schedule
# time_fromnow takes up DD:HH:MM format

# determine end time
def time_process(time_from_now):
  time_from_now = time_from_now.split(':')
  days = 0
  if(len(time_from_now) == 2):
    hours, minutes =  time_from_now[0], time_from_now[1]
  if(len(time_from_now) == 3):
    days, hours, minutes = time_from_now[0], time_from_now[1], time_from_now[2]
  return(datetime.utcnow() + timedelta(days = int(days), hours=int(hours), minutes = int(minutes)))

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title = "Help",
        description = "List of available commands.",
        timestamp = datetime.utcnow(),
        colour = discord.Colour.blue()
    )

    embed.set_author(name="Study Bot", icon_url="https://i.imgur.com/rdm3W9t.png")

    embed.add_field(name=f"adds a task to your schedule", value=f"`$add <task name> <time - HH:MM or DD:HH:MM>`", inline=False)
    embed.add_field(name=f"deletes task from your schedule", value=f"`$delete <task name>`", inline=False)
    embed.add_field(name=f"updates existing task", value=f"`$update <task name> <time - HH:MM or DD:HH:MM>`", inline=False)
    embed.add_field(name=f"marks task as complete", value=f"`$complete <task name>`", inline=False)
    embed.add_field(name=f"view current tasks", value=f"`$show`", inline=False)

    # embed.set_thumbnail(url="https://i.imgur.com/rdm3W9t.png")
    embed.set_footer(text="Study Bot®", icon_url="https://i.imgur.com/rdm3W9t.png")
    await ctx.send(embed=embed)

# add items to schedule
@client.command()
async def add(ctx, *, arg):
  print(ctx.author.id)
  task = " ".join(arg.split()[:-1])
  time = arg.split()[-1]
  print(task, time)
  comm = ("SELECT * FROM userlog WHERE item = %s AND user = %s")
  data = (str(task), str(ctx.author.id))
  mycursor.execute(comm, data)
  rows = mycursor.fetchall()
  if(len(rows) == 0):
    # process the time to calculate end date
    time = time_process(time)
    # adding item to database
    comm = (
    "INSERT INTO userlog (user, item, endtime) VALUES (%s, %s, %s)"
    )
    data = (str(ctx.author.id), str(task), str(time))
    mycursor.execute(comm, data)
    mycursor.execute("SELECT * FROM userlog")
    rows = mycursor.fetchall()
    print(rows)
    await ctx.send(f"You have added **{str(task)}** successfully!")
    with open('tasks.csv') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter = ",")
      #print("NUMBER OF TASKS: " + str(csv_reader))
      data = ""
      for row in csv_reader:
        for j in row:
          data += j
    data = int(data) + 1
    print("NUMBER OF TASKS: " + str(data))
    with open('tasks.csv', mode='w') as csv_file:
      csv_write = csv.writer(csv_file)
      csv_write.writerow(str(data))
  else:
    await ctx.send("You already have a task by that name pending. If you would like to override this task please update it using the update command.")

# delete items from schedule
@client.command()
async def delete(ctx, *, task):
  data = (str(ctx.author.id), str(task))
  comm = (
    "SELECT * FROM userlog where user = %s AND item = %s"
  )
  mycursor.execute(comm, data)
  rows = mycursor.fetchall()
  if(len(rows) == 0):
    await ctx.send("Your task **" + str(task) + "** does not exist!")
  else:
    comm = (
    "DELETE FROM userlog WHERE user = %s  AND item = %s"
    )
    mycursor.execute(comm, data)
    await ctx.send(f"Deleted **{task}**.")

# update items
@client.command()
async def update(ctx, *, arg):
  task = " ".join(arg.split()[:-1])
  new_time = arg.split()[-1]
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
    await ctx.send(f"You have updated **{str(task)}**.")

# calc diffs
async def timeDifferential(time_curr, time_lat):
  time_lat = time_lat.split('.')[0]
  time_lat = datetime.strptime(time_lat, '%Y-%m-%d %H:%M:%S')
  t_diff = time_lat - time_curr
  seconds = -1 * (t_diff.seconds + t_diff.days * 86400)
  minutes = int(seconds / 60)
  days = int(minutes / 1440)
  minutes = minutes -  days * 1440
  hours = int(minutes / 60)
  minutes = minutes - hours * 60
  return(-1*days, -1*hours, -1*minutes)

# show user tasks
@client.command()
async def show(ctx):
  comm = (
  "SELECT * FROM userlog WHERE user = %d"
  )
  data = (ctx.author.id)
  print(ctx.author.id)
  mycursor.execute(comm % (data))
  userMention = ctx.author.mention
  rows = sorted([row[1:] for row in mycursor.fetchall()], key=lambda x: datetime.strptime(str(x[1]).split(".")[0], '%Y-%m-%d %H:%M:%S'))
  print("Rows: ", rows)
  row_new = []
  for row in rows:
    days, hours, minutes = await timeDifferential(datetime.utcnow(), row[1])
    rv = ""
    if(days != 0):
      rv += str(days) + " days "
    if(hours != 0):
      rv += str(hours) + " hrs "
    if(minutes != 0):
      rv += str(minutes) + " mins "
    row_new.append((row[0], rv))
    row = (row[0], rv)
    print(rv)
    print(row)
    #here you need to replace the row time entry with RV.
    print(days, hours, minutes)
  rows = row_new
  print("New Rows: ", rows)
  if(len(rows) == 0):
    await ctx.send(f"{userMention} currently, you have no tasks. Please add items to view your current task list.")
  else:
    await ctx.send(userMention)
    embed = discord.Embed(
        title = "Here are your tasks. :notepad_spiral:",
        timestamp = datetime.utcnow(),
        colour = discord.Colour.blue()
    )

    embed.set_author(name="Study Bot", icon_url="https://i.imgur.com/rdm3W9t.png")

    for row in rows:
        embed.add_field(name=f"`{row[0]}`", value=f"{row[1]}", inline=False)

    # embed.set_thumbnail(url="https://i.imgur.com/rdm3W9t.png")
    embed.set_footer(text="Study Bot®", icon_url="https://i.imgur.com/rdm3W9t.png")
    await ctx.send(embed=embed)
    # await ctx.send(userMention)
    # await ctx.send("\n".join([str(row) for row in rows]))

# indicate that item is completed
@client.command()
async def complete(ctx, *, task):
  data = (str(ctx.author.id), str(task))
  comm = (
    "SELECT * FROM userlog where user = %s AND item = %s"
  )
  mycursor.execute(comm, data)
  rows = mycursor.fetchall()
  if(len(rows) == 0):
    await ctx.send("Your task **" + str(task) + "** does not exist!")
  else:
    comm = (
    "DELETE FROM userlog WHERE user = %s  AND item = %s"
    )
    mycursor.execute(comm, data)
    await ctx.send(f"Congrats you completed **{task}** successfully :partying_face:")

# info for users
@client.command()
async def info(ctx):
  embed = discord.Embed(
    title = "Info",
    description = "Statistics for Study Bot",
    timestamp = datetime.utcnow(),
    colour = discord.Colour.blue()
  )
  with open('tasks.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ",")
    #print("NUMBER OF TASKS: " + str(csv_reader))
    data = ""
    for row in csv_reader:
      for j in row:
        data += j

  embed.set_author(name="Study Bot", icon_url="https://i.imgur.com/rdm3W9t.png")
  embed.add_field(name=f"Total Tasks Created", value=f"{data}", inline=False)

  # embed.set_thumbnail(url="https://i.imgur.com/rdm3W9t.png")
  embed.set_footer(text="Study Bot®", icon_url="https://i.imgur.com/rdm3W9t.png")
  await ctx.send(embed=embed)

#dont touch the below tings
client.run(f"{credentials[4]}")
