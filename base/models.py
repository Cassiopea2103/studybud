from django.db import models
from django.contrib.auth.models import AbstractUser  


# User class : 
class User ( AbstractUser ) : 
    name = models.CharField ( max_length = 200 , null = True, blank = True ) 
    email = models.EmailField ( unique = True , null = True , blank = False ) 
    bio = models.TextField ( blank = True , null = True ) 
    avatar = models.ImageField ( null = True , blank = True , default = "avatar.svg" ) 

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = [ ] 

# Topic : 
class Topic ( models.Model ) : 
    name = models.CharField( max_length = 50 ) 
    
    def __str__ ( self ) : 
        return self.name 



# Room : 
class Room ( models.Model ) : 
    host = models.ForeignKey ( User , on_delete = models.SET_NULL , null = True )
    participants = models.ManyToManyField ( User , related_name = "participants" , blank = True )
    topic = models.ForeignKey ( Topic , on_delete = models.SET_NULL , null = True )  
    name = models.CharField ( max_length = 75 ) 
    description = models.TextField ( null = True , blank = True ) 
    created = models.DateTimeField ( auto_now_add = True ) 
    updated = models.DateTimeField ( auto_now = True ) 

    def __str__ ( self ) : 
        return self.name
    

    class Meta : 
        ordering = [ '-updated' , '-created']


# Message : 
class Message ( models.Model ) : 
    sender = models.ForeignKey ( User , on_delete = models.CASCADE ) 
    room = models.ForeignKey ( Room , on_delete = models.CASCADE ) 
    body = models.TextField ( ) 
    created = models.DateTimeField ( auto_now_add = True ) 
    updated = models.DateTimeField ( auto_now = True ) 

    def __str__ ( self ) : 
        return self.body[0 : 25] + "..." 
    
    class Meta : 
        ordering = [ "-updated" , "-created" ]

