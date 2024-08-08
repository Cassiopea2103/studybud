from django.shortcuts import render
from django.http import request 

# Home page : 
def home ( request ) : 
    return render ( request , "base/home.html" )