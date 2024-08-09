from django.forms import ModelForm 
from .models import Room 


# RoomForm 
class RoomForm ( ModelForm ) : 
    class Meta : 
        model = Room 
        fields = "__all__"