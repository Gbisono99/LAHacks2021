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
events = [] #A list of Event objects from information.py. Every event information.
all_people = [] #A list of Person objects from information.py. Basically each member's information.

guild_id = 824048886746185758 #Guild's current id.
guild_global = None #Initalized to None but on_ready() will set it to the given server.
#A list of Roles might be useful?
server_information = [] #Server information
def print_format(generic_list):
    description = ''
    for generic in generic_list:
        description = description + f' {generic.name}'
    return description
def member_to_person(member_list):
    new_list = []
    for member in member_list:
        new_list.append(Person(name = member.name,level = 0, exp =  0.0,roles = member.roles, date = member.joined_at))
    return new_list
def is_event_valid(event_name):
    for event in events:
        if event_name == event.name:
            return True
    return False
def find_role_object(role_list,role_name):
    for role in role_list:
        if role.name == role_name:
            return role
    return None
def find_list_index_people(people_list,person_name):
    for (index,person) in zip(range(0,len(people_list)-1,people_list)):
        if person.name == person_name:
            return index
    return -1

#Discord Events, not line 9.
@client.event
async def on_ready():
    
    guild_global = client.get_guild(guild_id) #Server information
    server_test = ServerInfomation(guild_global.name,guild_global.members,guild_global.roles,guild_global.text_channels,guild_global.voice_channels,events)
    server_information.append(ServerInfomation(guild_global.name,guild_global.members,guild_global.roles,guild_global.text_channels,guild_global.voice_channels,events))
    print(server_information[0].member_list)
    #Init all Members to Person Objects
    all_people.extend(member_to_person(guild_global.members))
    print(all_people)
    print('Bot is online.')

    
@client.event
async def on_member_join(member):
    all_people.append(Person(member.name,0,0.0,member.roles,member.joined_at))

#@Admins and @Event Organizers
@client.command()
async def server_info(ctx):
    info_name = server_information[0].name
    info_members = 'Members: \n' + print_format(server_information[0].member_list)+ '\n'
    info_roles = 'Roles: \n' + print_format(server_information[0].roles_list)+ '\n'
    info_texts = 'Texts: \n' + print_format(server_information[0].text_list)+ '\n'
    info_voices = 'Voices: \n' + print_format(server_information[0].voice_list)+ '\n'
    info_events = 'Current Events: \n' + print_format(server_information[0].curr_event_list)+ '\n'

    description = f'{info_members}\n{info_roles}\n{info_texts}\n{info_voices}\n{info_events}'
    embed = discord.Embed(title = f'{info_name}\'s Server Information', description = description)
    await ctx.send(embed = embed)
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
    for person in all_people:
        if(ctx.author.name == person.name):
            info_roles = 'Roles: \n' + print_format(person.roles)+ '\n'
            info_level = f'Level: {person.level} \n'
            info_exp = f'Experience: {person.exp} \n'
            info_date = f'Date Joined: {person.date} \n'
            description = f'{info_roles}\n{info_level}\n{info_exp}\n{info_date}'
            embed = discord.Embed(title = f'{person.name}\'s Information', description = description)
            await ctx.send(embed = embed)
@client.command()
async def join_event(ctx,event_name):
    if len(event_name) == 0:
        await ctx.send('No current events available')
    else:
        isValid = is_event_valid(event_name)
        if not isValid: #if false
            await ctx.send('Event name was invalid or does not exist')
        else:
            role_added = find_role_object(ctx.guild.roles,event_name)
            await ctx.author.add_roles(role_added)
            index = find_list_index_people(all_people, ctx.author.name)
            all_people[index].roles.append(role_added)

            index = find_list_index_people(events,event_name)
            events[index].participates.append(ctx.author)


@client.command()
async def leave_event(ctx,event_name):
    isValid = is_event_valid(event_name)
    if not isValid:
        await ctx.send('Event name was invalid or does not exist')
    else:
        role_remove = find_role_object(ctx.guild.roles, event_name)
        await ctx.author.remove_roles(role_remove)
        index = find_list_index_people(all_people, ctx.author.name)
        all_people[index].roles.remove(role_remove)

        index = find_list_index_people(events,event_name)
        events[index].participates.remove(ctx.author)
@client.command()
async def event_information(ctx,event_name):
    description = ''
    if len(events) == 0:
        await ctx.send('No current events available')
    else:
        for event in events:
            if event_name == event.name:
                description = description + f'Description:{event.event_description}\nPoints:{event.points}\nDate Created:{event.date}'
                embed = discord.Embed(title = f'{event.name}', description = description)
                await ctx.send(embed = embed)
            else:
                await ctx.send('Event not found')
@client.command()
async def all_events(ctx):
    description = ''
    for event in events:
        description = description + f'Name:{event.name}\nDescription:{event.event_description}\nPoints:{event.points}\n==========\n'
    embed = discord.Embed(title = f'All Events Information', description = description)
    await ctx.send(embed = embed)
client.run(token)

#Standard Methods

