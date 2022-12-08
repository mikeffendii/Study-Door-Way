from classes.models import ClassRoom,Student
from classes import views
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from chat.models import Message
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from rest_framework.response import Response
from .serializer import MessageSerializer
from .models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view 
from rest_framework import viewsets
import requests

@login_required
def course_chat_room(request,id):
	course = ClassRoom.objects.get(id=id)
	return render(request, 'chat/room.html',{'course':course})
  

class getMessages(viewsets.ModelViewSet):
	queryset=Message.objects.all()
	serializer_class=MessageSerializer


def getapidata(request):
	response=requests.get('http://127.0.0.1:8000/ajaxusers/').json()
	return render(request, 'chat/room.html',{'amir':response})



