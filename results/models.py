from django.db import models
from quizes.models import Quiz
from classes.models import ClassRoom,Student
from django.contrib.auth.models import User


class Result(models.Model):
	quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	class_room = models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
	score = models.FloatField()

	def __str__(self):
		return str(self.pk)