from rest_framework import serializers
from chat.models import Message,User
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
	author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
	class Meta:
		model=	Message
		fields = ('content','timestamp','author','class_room')






