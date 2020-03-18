import discord
import csv
from discord.ext import commands

client = discord.Client()
bot = commands.Bot("")

messagebs = []

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  guilds = client.guilds


# assume prefix to be "!"
a_prefix = "!"

@client.event
async def on_message(message):
  '''
  Example:
  message = "!add prenk 2h"
  prefix = "!"
  mess = ["add", "prenk", "2h"]
  '''
  prefix, mess = message.content[0:len(a_prefix)], message.content[len(a_prefix):]
  mess = " ".join(mess.split()).split(' ') #tf is htis prenk removes whitespace
  if(prefix == a_prefix): 
    messagebs.append(mess)
    print(messagebs)
    '''
    if(mess[0] == "add"): #add item
      messagebs.append(mess)
    if(mess[0] == "update") #update item
    if(mess[0] == "show") #show list of items 
    if(mess[0] == "delete") #delete kukkar
    if(mess[0] == "complete") #mark completion
    '''

  #message.content -> to extract the content of the message
  #message.author -> who wrote the message
  #await message.channel.send("the message you want to send") -> how to send a message to the channel
  if(message.content == "prenk"):
    await message.channel.send("prenk")
    await message.delete()


#dont touch the lines below

client.run("Njg5NzcwODc3OTk0NTMyODg0.XnHtRA.woz3RKnzeaztW2dTrhpbLekA68g")