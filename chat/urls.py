from django.urls import path
from . import views
app_name = 'chat'

urlpatterns = [

	path('room/<int:id>/', views.course_chat_room,name='course_chat_room'),
	path('room/getapidata/', views.getapidata,name='getapidata'),


	
]