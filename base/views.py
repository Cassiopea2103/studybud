from django.shortcuts import render , redirect 
from django.http import request 
from .models import Room , Topic
from .forms import RoomForm 


# Home page : 
def home ( request ) : 


    topics = Topic.objects.all () 
    
    topic_query = ''
    if request.GET.get( 'topic' ) is not None :
        topic_query = request.GET.get( 'topic' )
    
    rooms = Room.objects.filter ( topic__name__icontains = topic_query )
    rooms_count = rooms.count () 


    context = { "rooms" : rooms , "rooms_count" : rooms_count ,  "topics" : topics } 

    return render ( request , "base/home.html" , context )

# Single room page : 
def room ( request , room_id ) :
    
    room = Room.objects.get ( id = room_id ) 

    if room is not None : 
        context = { "room" : room }
     
    return render ( request , "base/room.html" , context  )


# Create Room : 
def create_room ( request ) : 

    # intial empty room form : 
    room_form = RoomForm () 

    if request.method == "POST" :
        # infer form with request data : 
        room_form = RoomForm ( request.POST ) 

        # check for form validity : 
        if room_form.is_valid : 
            # save it then : 
            room_form.save () 
            # redirect user to home page : 
            return redirect ( 'home')

    context = { 'room_form' : room_form , 'button' : 'Create room'}


    return render ( request , 'base/create_update_room.html' , context ) 


# update room : 
def update_room ( request , room_id ) : 

    # retrieve specific room with id :  
    found_room = Room.objects.get ( id = room_id ) 

    # intiialize room with prefilled data :
    room_form = RoomForm ( instance = found_room ) 

    if request.method == 'POST':
        # change form data with request data : 
        room_form = RoomForm ( request.POST , instance = found_room ) 
        
        # check form validity : 
        if room_form.is_valid () : 
            # save it : 
            room_form.save () 
            # redirect user to home page : 
            return redirect ( 'home' ) 
        
    context = { 'room_form': room_form , 'button' : 'Update room'}
        
    return render ( request , 'base/create_update_room.html' , context )



# delete room : 
def delete_room ( request , room_id ) : 

    # retrieve room : 
    room = Room.objects.get ( id = room_id )
    
    if request.method == 'POST' : 
        room.delete () 

        # redirect user to home page : 
        return redirect ( 'home' ) 

    context = { 'object' : room }

    return render ( request , 'base/delete_object.html' , context )