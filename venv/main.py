# import dependencies
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import requests
import json

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# set bot prefix
client = commands.Bot(command_prefix='!', intents=intents)

# channel ids
welcomeID = 0


# events
# read bot is online, terminal view
@client.event
async def on_ready():
    print("PlanetCS Bot Online")
    print("-------------------")


# welcome message
@client.event
async def on_member_join(member):
    channel = client.get_channel(welcomeID)
    await member.send("Welcome" + member + "to the PlanetCS Discord!")


# join voice channel
@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('')
        player = voice.play(source)
    else:
        await ctx.send("No Channel Found")


# disconnect voice channel
@client.command(pass_context=True)
async def disconnect(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Disconnected From Channel")
    else:
        await ctx.send("Currently not in a Voice Channel")


# client token
client.run('MTE3MDIwNjcxNDM0MDA1NzE4OQ.GL47nj.y0UtXrDSldxvUYMFmh6eElWHlR1nBBTXSE0fBA')
