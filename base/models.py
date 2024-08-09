from django.db import models
from django.contrib.auth.models import User 

# Topic : 
class Topic ( models.Model ) : 
    name = models.CharField( max_length = 50 ) 
    
    def __str__ ( self ) : 
        return self.name 



# Room : 
class Room ( models.Model ) : 
    host = models.ForeignKey ( User , on_delete = models.SET_NULL , null = True )
    # participants = models.ForeignKey ( User , )
    topic = models.ForeignKey ( Topic , on_delete = models.SET_NULL , null = True )  
    name = models.CharField ( max_length = 75 ) 
    description = models.TextField ( null = True , blank = True ) 
    created = models.DateTimeField ( auto_now_add = True ) 
    updated = models.DateTimeField ( auto_now = True ) 

    def __str__ ( self ) : 
        return self.name
    


# Message : 
class Message ( models.Model ) : 
    sender = models.ForeignKey ( User , on_delete = models.CASCADE ) 
    room = models.ForeignKey ( Room , on_delete = models.CASCADE ) 
    body = models.TextField ( ) 
    created = models.DateTimeField ( auto_now_add = True ) 
    updated = models.DateTimeField ( auto_now = True ) 

    def __str__ ( self ) : 
        return self.body[0 : 25] + "..." 

