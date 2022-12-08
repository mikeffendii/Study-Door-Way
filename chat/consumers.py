import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync 
from django.utils import timezone
from .models import Message
from classes.models import ClassRoom

class ChatConsumer(WebsocketConsumer):
	def connect(self):
		self.user = self.scope['user']
		self.id = self.scope['url_route']['kwargs']['id']
		self.room_group_name = 'chat_%s' % self.id
		# join room group
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)
		# accept connection
		self.accept()
	
	def disconnect(self, close_code):
		# leave room group
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)
		
	
	# receive message from WebSocket
	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		class_room = ClassRoom.objects.get(id=self.scope['url_route']['kwargs']['id'])
		now = timezone.now()
		Message.objects.create(author=self.scope['user'], content=message, timestamp=now,class_room=class_room).save()



		# send message to room group
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'user': self.user.username,
				'datetime': now.isoformat(),
			}
		)

	# receive message from room group
	def chat_message(self, event):
		# Send message to WebSocket
		self.send(text_data=json.dumps(event))



