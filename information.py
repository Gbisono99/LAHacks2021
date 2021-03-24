class Event:
    def __init__(self,name,event_description,points):
        self.name = name #The events name
        self.event_description = event_description #The events description
        self.points = points #The amount of points that are given per completion of said event.
class Person:
    def __init__(self,name,level,roles,date):
        self.name = name #Member's name
        self.level = level #Member's level
        self.roles = roles #this is a list of Role objects; A list of the Member's current role
        self.date = date #Member's joined date
class ServerInfomation:
    def __init__(self,name,member_list,roles_list,text_list,voice_list,curr_event_list):
        #Member List
        #Roles
        #Text Channels
        #Voice Channels
        #Current Events
        self.name = name
        self.member_list = member_list
        self.roles_list = roles_list
        self.text_list = text_list
        self.voice_list = voice_list
        self.curr_event_list = curr_event_list

