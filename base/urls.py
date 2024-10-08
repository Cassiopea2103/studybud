from django.urls import path 
from . import views 


urlpatterns = [
    path ( "register/" , views.userRegister , name = "register" ) ,
    path ( "login/" , views.userLogin ,name = "login") ,
    path ( "logout/" , views.logoutUser , name = "logout" ) ,

    path ( "user_profile/<str:user_id>" , views.user_profile , name = "user_profile" ) ,
    path ( "update_user/" , views.update_user , name = "update_user" ) ,

    path ( "" , views.home , name = "home" ) , 

    path ( "room/<str:room_id>", views.room , name = "room" ) ,
    path ( "create_room" , views.create_room , name = "create_room" ) ,
    path ( "update_room/<str:room_id>" , views.update_room , name = "update_room" ) ,
    path ( "delete_room/<str:room_id>" , views.delete_room , name = "delete_room" ) ,

    path ( "delete_message/<str:message_id>" , views.delete_message , name = "delete_message"),

    path ( "topics_list" , views.topics_list , name = "topics_list" ) ,
    path ( "activities" , views.activities , name = "activities" ) ,
    
]