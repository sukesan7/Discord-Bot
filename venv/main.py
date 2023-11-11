# import dependencies
import discord
import requests
import json
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import FFmpegPCMAudio
from discord import Member
from better_profanity import profanity

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# dictionary
queues = {}


def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)


# set bot prefix
client = commands.Bot(command_prefix='!', intents=intents)

# channel ids
welcomeID = 0
logsID = 0


# Events --------------------------------
# read bot is online, terminal view
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game('Counter Strike 2'))
    print("PlanetCS Bot Online")
    print("-------------------")


# welcome message
@client.event
async def on_member_join(member):
    channel = client.get_channel(welcomeID)
    await member.send("Welcome" + member + "to the PlanetCS Discord!")


# Logger -------------------------------- (WORK IN PROGRESS)
# member leave
@client.event
async def on_member_remove(member):
    channel = client.get_channel(logsID)
    await member.send(member + "has left the server")


# member update
@client.event
async def on_member_update(before, after):
    channel = client.get_channel(logsID)


# user update
@client.event
async def on_user_update(before, after):
    channel = client.get_channel(logsID)


# message deletion
@client.event
async def on_message_delete(message):
    channel = client.get_channel(logsID)

# custom message detection


# Moderation --------------------------------
# kick users
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked')


# kick users error
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No permission")


# Audio Commands --------------------------------
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


# pause audio
@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No Audio Playing")


# resume audio
@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("No Audio Paused")


# stop audio
@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


# play audio
@client.command(pass_context=True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))


# queue audio
@client.command(pass_context=True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg
    source = FFmpegPCMAudio(song)
    guild_id = ctx.message.guild.id
    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]
    await ctx.send("Added to the queue")


# Embeds --------------------------------
@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Embed Title", url=None, description="description", color=0xff0000)
    embed.set_author(name=ctx.author.display_name, url=None, icon_url=ctx.message.author.avatar.url)
    embed.set_thumbnail(url="https://www.adorama.com/alc/wp-content/uploads/2015/05/stories-HRX5WXFyB64-unsplash.jpg")
    await ctx.send(embed=embed)


# client token
client.run('')
