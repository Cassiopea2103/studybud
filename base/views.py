from django.shortcuts import render , redirect 
from django.http import request 
from django.db.models import Q 
from django.contrib import messages 

from .models import Room , Topic
from .forms import RoomForm 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate , login , logout 

# register user : 
def userRegister ( request ) : 

    context = {}
    
    return render ( request , 'base/login_register.html' , context  )

# Login : 
def userLogin ( request ) : 
    
    # retrieve the request data : 
    if request.method == 'POST':
        username = request.POST.get ( 'username' )
        password = request.POST.get ( 'password' )

        # try to find the user : 
        try :
            found_user = User.objects.get ( username = username ) 

            # authenticate the user : 
            found_user = authenticate ( request , username = username , password = password ) 

            # login the user : 
            if found_user is not None : 
                login ( request , found_user ) 

                # redirect to home page : 
                return redirect ( 'home' ) 

            else : 
                # create an authentication error message : 
                messages.error ( request , "Wrong password" )  
        except : 
            messages.error ( request , "User does not exist" )

        
       
    
    
    context = {} 
    return render ( request , 'base/login_register.html', context )


# logout : 
def logoutUser ( request ) : 

    logout ( request )
    
    return redirect ( 'home' ) 



# Home page : 
def home ( request ) : 


    topics = Topic.objects.all () 
    
    query = ''
    if request.GET.get( 'query' ) is not None :
        query = request.GET.get( 'query' )
    
    rooms = Room.objects.filter ( 
        Q ( topic__name__icontains = query ) | 
        Q ( name__icontains = query ) | 
        Q ( host__username__icontains = query )
     )
    rooms_count = rooms.count () 


    context = { "rooms" : rooms , "rooms_count" : rooms_count ,  "topics" : topics } 

    return render ( request , "base/home.html" , context )

# Single room page : 
def room ( request , room_id ) :
    
    room = Room.objects.get ( id = room_id ) 

    if room is not None : 
        context = { "room" : room }
     
    return render ( request , "base/room.html" , context  )

@login_required  ( login_url = "login" )
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