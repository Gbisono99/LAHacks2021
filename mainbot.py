import discord
from discord import Role
from discord.abc import GuildChannel
from discord.ext import commands
from discord.client import Client
from discord.guild import Guild
from discord.ext.commands import Context
import asyncio
from information import Event
from information import Person


intents = discord.Intents.all()
client = commands.Bot(command_prefix = '$', intents = intents)
token = 'ODI0MDM3OTc5MTMwNjkxNjI0.YFpjLA.0fkY4p7btGEDgaetEfHNVosI0B0'
events = {} #Key = event name,  value = Event object from information.py
all_people = [] #A list of Person objects from information.py. Basically each member's information.

guild_id = 824048886746185758 #Guild's current id.
server = None #Initalized to None but on_ready() will set it to the given server.
#A list of Roles might be useful?

#Discord Events, not line 9.
@client.event
async def on_ready():
    print('Bot is online.')
    server = client.get_guild(guild_id) #Server information
@client.event
async def on_member_join(member):
    pass

#@Admins and @Event Organizers
@client.command()
async def server_info(ctx):
    pass
@client.command()
async def event_create(ctx):
    pass
@client.command()
async def event_delete(ctx):
    pass
@client.command()
async def points_for_role(ctx):
    pass
@client.command()
async def update_json(ctx):
    pass
@client.command()
async def assign_for_points(ctx):
    pass
#@everyone
@client.command()
async def member_info(ctx):
    pass
@client.command()
async def join_event(ctx,event):
    pass
@client.command()
async def leave_event(ctx,event):
    pass
@client.command()
async def event_information(ctx,event):
    pass

client.run(token)