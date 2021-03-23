class Event:
    def __init__(self,event_name,event_description,points):
        self.event_name = event_name #The events name
        self.event_description = event_description #The events description
        self.points = points #The amount of points that are given per completion of said event.
class Person:
    def __init__(self,member_id,level,roles,date):
        self.member_id = member_id #Member's name
        self.level = level #Member's level
        self.roles = roles #this is a list of Role objects; A list of the Member's current role
        self.date = date #Member's joined date