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
from information import ServerInfomation


intents = discord.Intents.all()
client = commands.Bot(command_prefix = '\\', intents = intents)
token = 'ODI0MDM3OTc5MTMwNjkxNjI0.YFpjLA.0fkY4p7btGEDgaetEfHNVosI0B0'
events = {} #Key = event name,  value = Event object from information.py
all_people = [] #A list of Person objects from information.py. Basically each member's information.

guild_id = 824048886746185758 #Guild's current id.
guild_global = None #Initalized to None but on_ready() will set it to the given server.
#A list of Roles might be useful?
server_information = [] #Server information

#Discord Events, not line 9.
@client.event
async def on_ready():
    print('Bot is online.')
    guild_global = client.get_guild(guild_id) #Server information
    server_information.append(ServerInfomation(guild_global.name,guild_global.members,guild_global.roles,guild_global.text_channels,guild_global.voice_channels,events))
    print(server_information[0].member_list)
@client.event
async def on_member_join(member):
    pass

#@Admins and @Event Organizers
@client.command()
async def server_info(ctx):
    temp = serverformat(server_information[0].member_list)
    #info_members = f'Members: \n {temp} \n'
    #info_roles = 'Roles: \n' + serverformat(server_information.roles_list) + '\n'
    #info_texts = 'Texts: \n' + serverformat(server_information.texts_list) + '\n'
    #info_voices = 'Voices: \n' + serverformat(server_information.voice_list) + '\n'
    #info_events = 'Current Events: \n' + serverformat(server_information.curr_event_list) + '\n'

    #description = f'{info_members}+{info_roles}+{info_texts}+{info_voices}+{info_events}'
    #embed = discord.Embed(title = f'{server_information.name}\'s Server Information', description = description)
    #await ctx.send(embed = embed)
@client.command()
async def event_create(ctx):
    pass
@client.command()
async def event_delete(ctx):
    pass
@client.command()
async def points_for_role(ctx):
    pass
#@client.command()
#async def update_json(ctx):
#    pass
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
@client.command()
async def all_events(ctx):
    pass
client.run(token)

#Standard Methods
def serverformat(generic_list):
    description = ''
    #if generic_list != None:
    for generic in generic_list:
        description = description + f'{generic.name}, '
    return description     
    #else:
        #return f'No given information available.'