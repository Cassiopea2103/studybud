from .models import Message 
from django.dispatch import receiver 
from django.db.models.signals import post_delete 


@receiver ( post_delete , sender = Message ) 
def remove_message_sender_from_participants ( sender , instance , **kwargs ) : 
    
    if not Message.objects.filter ( sender = instance.sender , room = instance.room ) :
        instance.room.participants.remove ( instance.sender ) 