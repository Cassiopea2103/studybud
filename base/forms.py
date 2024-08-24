from django.forms import ModelForm 
from .models import User , Room 
from django.contrib.auth.forms import UserCreationForm  


# Custom user creation form : 
class MyUserCreationForm ( UserCreationForm ) : 
    class Meta : 
        model = User 
        fields = [ "username" ,  "name" , "email" , "password1" , "password2" ]
        exclude = [ "usable_password" ]

#UserForm : 
class UserForm ( ModelForm ) : 
    class Meta : 
        model = User 
        fields = [ "username" , "name" , "email" , "bio" , "avatar" ]


# RoomForm 
class RoomForm ( ModelForm ) : 
    class Meta : 
        model = Room 
        fields = "__all__"
        exclude = [ "host" , "participants" ]