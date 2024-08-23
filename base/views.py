from django.shortcuts import render , redirect 
from django.http import request 
from django.http.response import HttpResponse 
from django.db.models import Q 
from django.contrib import messages 

from .models import Room , Topic , Message 
from .forms import RoomForm 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate , login , logout 

# register user : 
def userRegister ( request ) : 
    page = "register"

    # new user creation form object : 
    user_form = UserCreationForm () ; 

    # check if request method is POST : 
    if request.method == "POST" : 
        # fill user creation form with request data : 
        user_form = UserCreationForm ( request.POST ) 

        # check form data validity : 
        if user_form.is_valid () : 
            # save the form - but don't commit yet : 
            new_user = user_form.save ( commit = False ) 

            # new user username to lowercase : 
            new_user.username = new_user.username.lower() 

            # now save the new user : 
            new_user.save () 

            # login the new user : 
            login ( request , new_user )

            # redirect to the home page : 
            return redirect ( "home" )

        # otherwise return flash message error on user form : 
        else :
            messages.error ( request , "An error happened with the new user registration!" )    

    context = { "page" : page , "user_form" : user_form }
    
    return render ( request , 'base/login_register.html' , context  )

# Login : 
def userLogin ( request ) : 

    page = "login"

    if request.user.is_authenticated : 
        return redirect ('home') 
    
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

            
    
    context = { "page" : page  } 
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
    rooms_messages = Message.objects.all ().filter ( 
        Q ( room__topic__name__icontains = query ) |
        Q ( room__name = query ) | 
        Q ( sender__username = query )
    ) ; 


    context = { 
        "rooms" : rooms , 
        "rooms_count" : rooms_count ,  
        "topics" : topics , 
        "rooms_messages" : rooms_messages
    } 

    return render ( request , "base/home.html" , context )

# Single room page : 
def room ( request , room_id ) :
    
    # try to fetch the room in the database : 
    try : 
        room = Room.objects.get ( id = room_id ) 

        # collect room messages : 
        room_messages = room.message_set.all()
        # collect room participants : 
        room_participants = room.participants.all()  

        # handle the message post creation : 
        if request.method == "POST" : 
            # create the new message item : 
            new_message = Message.objects.create (
                sender = request.user , 
                room = room , 
                body = request.POST.get ( "body" ) 
            )
            # add the request user ( message send ) to the room participants : 
            room.participants.add ( request.user ) 
            # return redirect to the single room page : 
            return redirect ( "room" , room_id = room.id ) 

        context = { "room" : room , "room_messages" : room_messages , "participants" : room_participants }

    except : 
        return HttpResponse ( "Room does not exist !" ) 
     
    return render ( request , "base/room.html" , context  )




@login_required  ( login_url = "login" )
# Create Room : 
def create_room ( request ) : 

    # intial empty room form : 
    room_form = RoomForm () 

    if request.method == "POST" :
        # fill form with request data : 
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

    # allow update only to room host : 
    if request.user != found_room.host :
        return HttpResponse ( "Sorry . You are not allowed here !" )

    if request.method == 'POST':
        # fill form with request data : 
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



@login_required ( login_url = "login" ) 
def delete_message ( request , message_id ) : 

    # retrieve the corresponding id message : 
    room_message = Message.objects.get ( id = message_id ) 

    # ensure request user is the same as message sender : 
    if request.user != room_message.sender : 
        return HttpResponse ( "Sorry ! You do not have enough permissions for this action!")
    
    
    # delete message : 
    if request.method == "POST" : 
        room_message.delete () 
        
        # redirect to home or room accordingly :
        previous_url = request.POST.get('previous_url')     
        print ( "previous url" , previous_url)

        if "room" in previous_url : 
            return redirect ( "room" , room_id = room_message.room.id )
        else :
            return redirect ( "home" )
    
    return render ( request , 'base/delete_object.html' , { "object" : room_message } )