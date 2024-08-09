from django.shortcuts import render
from django.http import request 
from .models import Room 



# Home page : 
def home ( request ) : 

    rooms = Room.objects.all () 
    context = { "rooms" : rooms } 

    return render ( request , "base/home.html" , context )

# Single room page : 
def room ( request , room_id ) :
    
    room = Room.objects.get ( id = room_id ) 

    if room is not None : 
        context = { "room" : room }
     
    return render ( request , "base/room.html" , context  )