from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *



def create_instructor(sender, instance, created, **kwargs):
	if created:
		classroom = ClassRoom.objects.get(id=instance.id)
		instructor = Instructor(instructor=instance.user,class_room=classroom)
		instructor.save()
		print("Instructor created")



def create_assignment_notification(sender, instance, created, **kwargs):
	if created:
		assignment = Assignment.objects.get(id=instance.id)
		class_room = ClassRoom.objects.get(id=instance.class_room.id)
		user = User.objects.get(id=instance.user.id)
		notification = Notification.objects.create(class_room=class_room,assignment=assignment,user=user,title='New Assignment')
		print("Assignment Notification created")

post_save.connect(create_assignment_notification,sender=Assignment)
post_save.connect(create_instructor,sender=ClassRoom)