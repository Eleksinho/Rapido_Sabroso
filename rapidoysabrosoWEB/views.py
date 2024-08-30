from django.shortcuts import render
from django.urls import path , include

def vista1(request):
  
    return render(request,'service/vista1.html')