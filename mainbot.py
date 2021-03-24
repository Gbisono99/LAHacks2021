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
import random


intents = discord.Intents.all()
client = commands.Bot(command_prefix = '$', intents = intents)
token = 'ODI0MDc1NjQzOTMwOTM1MzY2.YFqGQA.uiWUYo-81ICUvHbBdMtItd2ur6U'
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
async def event_create(ctx, *args):
    role_perm = discord.Permissions(view_channel=False)
    if(len(args) <= 2 and len(args) != 0):
        if len(args) == 2:
            role = await ctx.guild.create_role(name=args[0], colour=discord.Colour(color_value), permissions=role_perm)

        elif len(args) == 1:
            role = await ctx.guild.create_role(name=args[0], colour=discord.Colour(random.randint(0,255)), permissions=role_perm)
        event_category = await ctx.guild.create_category(name=args[0])
        await event_category.create_text_channel(name=args[0])
        await event_category.create_voice_channel(name=args[0])
        await category.set_permissions(role, read_messages=True, send_messages=True, connect=True, speak=True)
        await category.set_permissions(ctx.guild.default_role, read_messages=False, connect=False)
    else:
        await ctx.send(f'Expected 2 or 1 Input Arguments; Received {len(args)}')

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