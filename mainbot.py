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
import random


intents = discord.Intents.all()
client = commands.Bot(command_prefix = '\\', intents = intents, help_command = None)
token = 'ODI0MDM3OTc5MTMwNjkxNjI0.YFpjLA.1WX89fBb8-gGgQGlBiC-rzeAtA0'
events = [] #A list of Event objects from information.py. Every event information.
all_people = [] #A list of Person objects from information.py. Basically each member's information.
guild_id = 824048886746185758 #Guild's current id.
guild_global = client.get_guild(guild_id) #Initalized to None but on_ready() will set it to the given server.
#A list of Roles might be useful?
server_information = [] #Server information
level_list = [83,174,276,388,512] #List of level up.
def print_format(generic_list):
    description = ''
    for generic in generic_list:
        description = description + f' {generic.name}'
    return description
def member_to_person(member_list):
    new_list = []
    for member in member_list:
        new_list.append(Person(name = member.name,level = 0, exp =  0,roles = member.roles, date = member.joined_at))
    return new_list
def is_event_valid(event_name):
    for event in events:
        if event_name == event.name:
            return True
    return False
def find_object(object_list,object_name):
    for indv_object in object_list:
        if indv_object.name == object_name:
            return indv_object
    return None
def find_list_index_people(people_list,person_name):
    for (index,person) in zip(range(0,len(people_list)),people_list):
        if person.name == person_name:
            return index

#Discord Events, not line 9.
@client.event
async def on_ready():
    
    guild_global = client.get_guild(guild_id) #Server information
    server_test = ServerInfomation(guild_global.name,guild_global.members,guild_global.roles,guild_global.text_channels,guild_global.voice_channels,events)
    server_information.append(ServerInfomation(guild_global.name,guild_global.members,guild_global.roles,guild_global.text_channels,guild_global.voice_channels,events))
    #Init all Members to Person Objects
    all_people.extend(member_to_person(guild_global.members))
    if discord.utils.get(guild_global.roles,name = 'Event Organizer') is None:
        role_perm = discord.Permissions(view_channel = False)
        await guild_global.create_role(name='Event Organizer', colour= 0x00C422, permissions=role_perm)
    print('Bot is online.')

    #with open('data.txt', 'w') as json_file:
        #encodeJSON = jsonpickle.encode(server_information[0])
        #json.dump(encodeJSON, json_file, indent=4,sort_keys=True)
@client.event
async def on_member_join(member):
    all_people.append(Person(member.name,0,0.0,member.roles,member.joined_at))
@client.event
async def on_member_remove(member):
         pass
#@Admins and @Event Organizers
@client.command(aliases = ['sinfo','serverinfo','server'])
@commands.has_permissions(administrator =True)
async def server_info(ctx):
    info_name = server_information[0].name
    info_members = 'Members: \n' + print_format(server_information[0].member_list)+ '\n'
    info_roles = 'Roles: \n' + print_format(server_information[0].roles_list)+ '\n'
    info_texts = 'Texts: \n' + print_format(server_information[0].text_list)+ '\n'
    info_voices = 'Voices: \n' + print_format(server_information[0].voice_list)+ '\n'
    info_events = 'Current Events: \n' + print_format(server_information[0].curr_event_list)+ '\n'

    description = f'{info_members}\n{info_roles}\n{info_texts}\n{info_voices}\n{info_events}'
    embed = discord.Embed(title = f'{info_name}\'s Server Information', description = description, color = 0x00C422)
    await ctx.send(embed = embed)
# $events_create {event_name} {role_color} {event_description} {points}
@client.command(aliases = ['ecreate','createevent'])
@commands.has_role('Event Organizer')
async def event_create(ctx, *args):
    if(discord.utils.get(ctx.guild.roles, name=args[0]) is None):
        if(len(args) == 4):
            role_perm = discord.Permissions(view_channel=False)
            role = await ctx.guild.create_role(name=args[0], colour=discord.Colour(int(args[1], 16)), permissions=role_perm)
            event_org_role = discord.utils.get(ctx.guild.roles,name = 'Event Organizer')
            event_category = await ctx.guild.create_category(name=args[0])
            await event_category.create_text_channel(name=args[0])
            await event_category.create_voice_channel(name=args[0])
            await event_category.set_permissions(role, read_messages=True, send_messages=True, connect=True, speak=True)
            await event_category.set_permissions(event_org_role, read_messages=True, send_messages=True, connect=True, speak=True)
            await event_category.set_permissions(ctx.guild.default_role, read_messages=False, connect=False)
            event = Event(args[0], args[2], int(args[3], 10), [], role.created_at)
            events.append(Event(args[0], args[2], int(args[3], 10), [], role.created_at))
            embed = discord.Embed(title = 'Creating an Event', description = f'{event.name} has been created!', color = role.color)
            embed.add_field(name = 'Description', value = f'{event.event_description}')
            embed.add_field(name = 'Points', value = f'{event.points}')
            await ctx.send(embed = embed)

            
        elif(len(args) == 3):
            role_perm = discord.Permissions(view_channel=False)
            role = await ctx.guild.create_role(name=args[0], colour=discord.Colour(random.randint(0, 255)), permissions=role_perm)
            event_org_role = discord.utils.get(ctx.guild.roles,name = 'Event Organizer')
            event_category = await ctx.guild.create_category(name=args[0])
            await event_category.create_text_channel(name=args[0])
            await event_category.create_voice_channel(name=args[0])
            await event_category.set_permissions(role, read_messages=True, send_messages=True, connect=True, speak=True)
            await event_category.set_permissions(event_org_role, read_messages=True, send_messages=True, connect=True, speak=True)
            await event_category.set_permissions(ctx.guild.default_role, read_messages=False, connect=False)
            event = Event(args[0], args[1], int(args[2], 10), [], role.created_at)
            events.append(Event(args[0], args[1], int(args[2], 10), [], role.created_at))
            embed = discord.Embed(title = 'Creating an Event', description = f'{event.name} has been created!', color = role.color)
            embed.add_field(name = 'Description', value = f'{event.event_description}')
            embed.add_field(name = 'Points', value = f'{event.points}')
            await ctx.send(embed = embed)            
    else:
        embed = discord.Embed(title = f'Creating an Event', description = 'Event already exists!', color = 0xC70039)
        await ctx.send(embed = embed)   

@client.command(aliases = ['edelete','deleteevent'])
@commands.has_role('Event Organizer')
async def event_delete(ctx, arg):
    if len(events) == 0:
        embed = discord.Embed(title = f'Changing Points', description = 'No events are running! D:', color = 0xFBFBFB)
        await ctx.send(embed = embed)
    else:
        isValid = is_event_valid(arg)
        if isValid:
            role = find_object(ctx.guild.roles,arg)
            await discord.utils.get(ctx.guild.roles, name = arg).delete()
            await discord.utils.get(ctx.guild.text_channels, name = str(arg.lower())).delete()
            await discord.utils.get(ctx.guild.voice_channels, name = arg).delete()
            await discord.utils.get(ctx.guild.categories, name = arg).delete()
            removed_event = find_object(events,arg) #Using the role specific def for events.
            events.remove(removed_event)
            server_information[0].curr_event_list = events
            embed = discord.Embed(title = 'Deleting an Event', description = f'{removed_event.name} has been deleted. No points will be given.', color = role.color)
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = f'Changing Points', description = 'Not a valid event! D:', color = 0xC70039)
            await ctx.send(embed = embed)        
    #Try using server_information[0]
#@client.command()
#async def update_json(ctx):
#    pass
@client.command(aliases = ['epoints','changepointsevent'])
@commands.has_role('Event Organizer')
async def change_points(ctx, event_name, points):
    if len(events) == 0:
        embed = discord.Embed(title = f'Changing Points', description = 'No events are running! D:', color = 0xFBFBFB)
        await ctx.send(embed = embed)
    else:
        index = find_list_index_people(events,event_name)
        isValid = is_event_valid(event_name)
        if isValid:
            pre_points = events[index].points
            events[index].points = int(points,10)
            role = find_object(ctx.guild.roles,event_name)
            embed = discord.Embed(title = f'Changing Points', description = f'{event_name}\'s points have been updated!', color = role.color)
            embed.add_field(name = 'Previous value', value = f'{pre_points}')
            embed.add_field(name = 'New value', value = f'{events[index].points}')
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = f'Changing Points', description = 'Not a valid event! D:', color = 0xC70039)
            await ctx.send(embed = embed)
@client.command(aliases = ['eclose','closeevent'])
@commands.has_role('Event Organizer')
async def event_close(ctx, event_name):
    if len(events) == 0:
        embed = discord.Embed(title = f'Closing an Event', description = 'No events are running! D:', color = 0xFBFBFB)
        await ctx.send(embed = embed)
    else:
        isValid = is_event_valid(event_name)
        event_object = find_object(events, event_name)
        if isValid:
            for member in event_object.participates:
                person = find_object(all_people,member.name)
                index = find_list_index_people(all_people,person.name)
                pre_exp = person.exp
                person.exp = person.exp + event_object.points
                if person.level == len(level_list):
                    embed = discord.Embed(title = f'{person.name}', description = f'{person.name} has reached max level.', color = 0xD4AF37)
                    embed.add_field(name = 'Level', value = f'{person.level}')
                    embed.add_field(name = 'Experience', value = f'Previous: {pre_exp} --> Current: {person.exp}')
                    await ctx.send(embed = embed)
                else:
                    if person.exp >= level_list[person.level]:
                        person.level = int(person.level) + 1
                        embed = discord.Embed(title = f'{person.name}', description = f'{person.name} has reached Level: {person.level}!', color = 0xD4AF37)
                        embed.add_field(name = 'Level', value = f'{person.level}')
                        embed.add_field(name = 'Experience', value = f'Previous: {pre_exp} --> Current: {person.exp}')
                        await ctx.send(embed = embed)
                all_people[index] = person
            
            await discord.utils.get(ctx.guild.roles, name = event_name).delete()
            await discord.utils.get(ctx.guild.text_channels, name = str(event_name.lower())).delete()
            await discord.utils.get(ctx.guild.voice_channels, name = event_name).delete()
            await discord.utils.get(ctx.guild.categories, name = event_name).delete()
            removed_event = find_object(events,event_name) #Using the role specific def for events.
            events.remove(removed_event)
            server_information[0].curr_event_list = events

            embed = discord.Embed(title = 'Closing an Event', description = f'{event_name} has officially been closed. Thanks to all for participating!', color = 0x00C422)
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = f'Closing an Event', description = 'Not a valid event! D:', color = 0xC70039)
            await ctx.send(embed = embed)

#@everyone
@client.command(aliases = ['minfo', 'myinformation', 'mystats'])
async def member_info(ctx):
    for person in all_people:
        if(ctx.author.name == person.name):
            if len(ctx.author.roles) == 1:
                color = 0xFBFBFB
            else:
                color = ctx.author.roles[1].color
            embed = discord.Embed(title = f'{person.name}\'s Information', color = color)
            embed.add_field(name = 'Roles', value = print_format(person.roles), inline = False)
            embed.add_field(name = 'Level', value = f'{person.level}')
            embed.add_field(name = 'Experience', value = f'{person.exp}')
            embed.add_field(name = 'Date Joined', value = f'{person.date}', inline = False)
            await ctx.send(embed = embed)
@client.command(aliases = ['ejoin','jevent', 'joinevent'])
async def join_event(ctx,event_name):
    if len(events) == 0:
        embed = discord.Embed(title = f'Joining an Event', description = 'No events are running! D:', color = 0xFBFBFB)
        await ctx.send(embed = embed)
    else:
        isValid = is_event_valid(event_name)
        if not isValid: #if false
            embed = discord.Embed(title = f'Joining an Event', description = 'Not a valid event! D:', color = 0xC70039)
            await ctx.send(embed = embed)
        else:
            role_added = find_object(ctx.guild.roles,event_name)
            await ctx.author.add_roles(role_added)
            index = find_list_index_people(all_people, ctx.author.name)
            all_people[index].roles.append(role_added)
            index = find_list_index_people(events,event_name)
            events[index].participates.append(ctx.author)
            embed = discord.Embed(title = f'Name of Event: {event_name}', description = f'User: {ctx.author} has joined this event!', color = role_added.color)
            await ctx.send(embed = embed)

@client.command(aliases = ['eleave','levent','leaveevent'])
async def leave_event(ctx,event_name):
    if len(events) == 0:
        embed = discord.Embed(title = f'Leaving an Event', description = 'No events are running! D:', color = 0xFBFBFB)
        await ctx.send(embed = embed)
    else:
        isValid = is_event_valid(event_name)
        if not isValid:
            embed = discord.Embed(title = f'Leaving an Event', description = 'Not a valid event! D:', color = 0xC70039)
            await ctx.send(embed = embed)
        else:
            role_remove = find_object(ctx.guild.roles, event_name)
            await ctx.author.remove_roles(role_remove)
            index = find_list_index_people(all_people, ctx.author.name)
            all_people[index].roles.remove(role_remove)
            index = find_list_index_people(events,event_name)
            events[index].participates.remove(ctx.author)
            embed = discord.Embed(title = f'Name of Event: {event_name}', description = 'User: {ctx.author} has leave this event!', color = role_remove.color)
            await ctx.send(embed = embed)

@client.command(aliases = ['einfo','eventinfo'])
async def event_information(ctx,event_name):
    description = ''
    if len(events) == 0:
        embed = discord.Embed(title = f'Event Information', description = 'No events are running! D:', color = 0xFBFBFB)
        await ctx.send(embed = embed)
    else:
        isValid = is_event_valid(event_name)
        if isValid:
            event = find_object(events,event_name)
            role = find_object(ctx.guild.roles, event_name)
            info_participates = print_format(event.participates)
            value = f'Description:{event.event_description}\nPoints:{event.points}\nDate Created:{event.date}\nParticipants:{info_participates}'
            embed = discord.Embed(title = f'Event Information', description = f'Event Information on {event.name}', color = role.color)
            embed.add_field(name = f'Name of Event: {event.name}', value = value)
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = f'Event Information', description = 'Not a valid event! D:', color = 0xC70039)
            await ctx.send(embed = embed)

@client.command(aliases = ['aeinfo','alleventinfo'])
async def all_events(ctx):
    description = ''
    if len(events) == 0:
        embed = discord.Embed(title = f'All Events Information', description = 'No events are running! D:', color = 0xFBFBFB)
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title = f'All Events Information', description = f'Event Information on All Events', color = 0x00C422)
        for event in events:
            value = f'Description: {event.event_description}\nPoints: {event.points}'
            embed.add_field(name = f'Name of Event: {event.name}', value = value, inline = False)
        await ctx.send(embed = embed)

@client.command()
async def help(ctx):
    author_perm = ctx.author.guild_permissions
    embed = discord.Embed(title = f'Help Menu for Commands', description = 'Gives the available commands for Event Bot.', color = 0xFBFBFB)
    if author_perm.administrator == True:
        embed.add_field(name = 'Server information', value = f'Provides information on the Server\n Commands: \\server_info \\sinfo \\serverinfo \\server\n Instruction: \\<COMMAND>', inline = False)

        embed.add_field(name = 'Creating an Event', value = f'Create an Event\n Commands: \\event_create \\ecreate \\createevent\n Instruction: \\<COMMAND> <EVENT NAME> <COLOR IN HEX: 0xXXXXXX> <EVENT INFO: USE "<info>"> <EVENT POINTS>', inline = False)
        embed.add_field(name = 'Deleting an Event', value = f'Deletes an Event\n Commands: \\event_delete \\edelete \\deleteevent\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'Changing Points in Event', value = f'Change Points for an Event\n Commands: \\change_points \\epoints \\changepointsevent\n Instruction: \\<COMMAND> <EVENT NAME> <NEW POINT VALUE>', inline = False)
        embed.add_field(name = 'Closing an Event', value = f'Closes an Event\n Commands: \\event_close \\eclose \\closeevent\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)

        embed.add_field(name = 'Member Information', value = f'Displays your information\n Commands: \\member_info \\minfo \\myinformation \\mystats\n Instruction: \\<COMMAND>', inline = False)
        embed.add_field(name = 'Join an Event', value = f'Has you join an Event.\n Commands: \\join_event \\ejoin \\jevent \\joinevent\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'Leave an Event', value = f'Has you leave an Event.\n Commands: \\leave_event \\eleave \\levent \\leaveevent\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'Event Information', value = f'Gives information on an Event.\n Commands: \\event_information \\einfo \\eventinfo\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'All Live Events', value = f'Gives information on all live Events.\n Commands: \\all_events \\aeinfo \\alleventinfo\n Instruction: \\<COMMAND>', inline = False)
        await ctx.send(embed = embed)         
        
    elif discord.utils.get(ctx.author.roles, name = 'Event Organizer') is not None:
        embed.add_field(name = 'Creating an Event', value = f'Create an Event\n Commands: \\event_create \\ecreate \\createevent\n Instruction: \\<COMMAND> <EVENT NAME> <ROLE COLOR> <EVENT INFO> <EVENT POINTS>', inline = False)
        embed.add_field(name = 'Deleting an Event', value = f'Deletes an Event\n Commands: \\event_delete \\edelete \\deleteevent\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'Changing Points in Event', value = f'Change Points for an Event\n Commands: \\change_points \\epoints \\changepointsevent\n Instruction: \\<COMMAND> <EVENT NAME> <NEW POINT VALUE>', inline = False)
        embed.add_field(name = 'Closing an Event', value = f'Closes an Event\n Commands: \\event_close \\eclose \\closeevent\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)

        embed.add_field(name = 'Member Information', value = f'Displays your information\n Commands: \\member_info \\minfo \\myinformation \\mystats\n Instruction: \\<COMMAND>', inline = False)
        embed.add_field(name = 'Join an Event', value = f'Has you join an Event.\n Commands: \\join_event \\ejoin \\jevent \\joinevent\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'Leave an Event', value = f'Has you leave an Event.\n Commands: \\leave_event \\eleave \\levent \\leaveevent\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'Event Information', value = f'Gives information on an Event.\n Commands: \\event_information \\einfo \\eventinfo\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'All Live Events', value = f'Gives information on all live Events.\n Commands: \\all_events \\aeinfo \\alleventinfo\n Instruction: \\<COMMAND>', inline = False)
        await ctx.send(embed = embed)            
    else:
        embed.add_field(name = 'Member Information', value = f'Displays your information\n Commands: \\member_info \\minfo \\myinformation \\mystats\n Instruction: \\<COMMAND>', inline = False)
        embed.add_field(name = 'Join an Event', value = f'Has you join an Event.\n Commands: \\join_event \\jevent \\ejoin \\joinevent\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'Leave an Event', value = f'Has you leave an Event.\n Commands: \\leave_event \\levent \\eleave \\leaveevent\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'Event Information', value = f'Gives information on an Event.\n Commands: \\event_information \\einfo \\eventinfo\n Instruction: \\<COMMAND> <EVENT NAME>', inline = False)
        embed.add_field(name = 'All Live Events', value = f'Gives information on all live Events.\n Commands: \\all_events \\aeinfo \\alleventinfo\n Instruction: \\<COMMAND>', inline = False)
        await ctx.send(embed = embed)
    
client.run(token)