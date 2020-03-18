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






#dont touch the lines below

client.run("Njg5NjgwOTY2ODMwMzkxMzA0.XnGfew.zTwns19a74uIQYqRKQZ8DHE6Xj0")