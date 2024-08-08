from django.shortcuts import render
from django.http import request 

# rooms data : 
rooms = [
    {"id" : 1 , "name" : "Python web dev" } , 
    {"id" : 2 , "name" : "React JS " } , 
    {"id" : 3 , "name" : "Springboot lovers" } , 
    {"id" : 4 , "name" : "Redux optimization" } , 
]

# Home page : 
def home ( request ) : 
    
    context = { "rooms" : rooms } 
    return render ( request , "base/home.html" , context )

# Single room page : 
def room ( request , room_id ) :
    room = None 

    for room_item in rooms : 
        if room_item["id"] == int (room_id )  : 
            room = room_item

    context = { "room" : room }
     
    return render ( request , "base/room.html" , context  )