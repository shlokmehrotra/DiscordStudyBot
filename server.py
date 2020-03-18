import discord
import csv
from discord.ext import commands


client = discord.Client()
bot = commands.Bot("")
infoarr = []
political_events = ["politic", "yang", "hillary", "trump", "liberal", "libtard", "leftist", "rightist", "tulsi", "democrats", "yengu", "yeng", "poll", "veto", "ynag", "y4ng"]
memes = ["instagram", "reddit"]
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    guilds = client.guilds
@client.event
async def on_message(message):
	#message.content -> to extract the content of the message
	#message.author -> who wrote the message
	#await message.channel.send("the message you want to send") -> how to send a message to the channel
	if(message.content == "prenk"):
		await message.channel.send("prenk")
	#here do whatever you want with the new message





#dont touch the lines below

client.run("Njg5NzcwODc3OTk0NTMyODg0.XnHtRA.woz3RKnzeaztW2dTrhpbLekA68g")