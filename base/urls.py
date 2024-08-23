from django.urls import path 
from . import views 


urlpatterns = [
    path ( "register/" , views.userRegister , name = "register" ) ,
    path ( "login/" , views.userLogin ,name = "login") ,
    path ( "logout/" , views.logoutUser , name = "logout" ) ,

    path ( "" , views.home , name = "home" ) , 

    path ( "room/<str:room_id>", views.room , name = "room" ) ,
    path ( "create_room" , views.create_room , name = "create_room" ) ,
    path ( "update_room/<str:room_id>" , views.update_room , name = "update_room" ) ,
    path ( "delete_room/<str:room_id>" , views.delete_room , name = "delete_room" ) ,

    path ( "delete_message/<str:message_id>" , views.delete_message , name = "delete_message")
    
]