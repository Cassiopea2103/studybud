from django.forms import ModelForm 
from .models import User , Room 
from django.contrib.auth.forms import UserCreationForm  


# Custom user creation form : 
class MyUserCreationForm ( ModelForm ) : 
    class Meta : 
        model = User 
        fields = [ "username" , "name" , "email" , "bio" , "avatar" ]

#UserForm : 
class UserForm ( ModelForm ) : 
    class Meta : 
        model = User 
        fields = [ "username" , "email" ]


# RoomForm 
class RoomForm ( ModelForm ) : 
    class Meta : 
        model = Room 
        fields = "__all__"
        exclude = [ "host" , "participants" ]