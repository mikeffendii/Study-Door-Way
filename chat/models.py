from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from classes.models import ClassRoom


class Message(models.Model):
	author = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
	content=models.CharField(max_length=100)
	timestamp=models.DateTimeField(auto_now_add=True)
	class_room = models.ForeignKey(ClassRoom,null=True,on_delete=models.CASCADE,related_name="messages")


	def __str__(self):
		return self.author.username
  

	# def last_10_messages(self):
	# 	return Message.objects.order_by('-timestamp').all()[:10]