import discord
from discord import Role
from discord.abc import GuildChannel
from discord.ext import commands
from discord.client import Client
from discord.guild import Guild
from discord.ext.commands import Context
import asyncio


intents = discord.Intents.all()
client = commands.Bot(command_prefix = '$', intents = intents)
token = 'ODI0MDM3OTc5MTMwNjkxNjI0.YFpjLA.0fkY4p7btGEDgaetEfHNVosI0B0'

@client.event
async def on_ready():
    print('Bot is online.')


#@Admins and @Event Organizers
@client.client
async def on_member_join(member):
    pass
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
@client.command()
async def member_info(ctx):
    pass
#@everyone
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