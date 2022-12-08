from django.db import models
import random
from classes.models import ClassRoom
from django.contrib.auth.models import User


DIFF_CHOICES = (
	('easy', 'easy'),
	('medium', 'medium'),
	('hard', 'hard'),
)



class Quiz(models.Model):
	name = models.CharField(max_length=120)
	topic = models.CharField(max_length=120)
	created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
	number_of_questions = models.IntegerField()
	class_room = models.ForeignKey(ClassRoom,null=True,on_delete=models.CASCADE)
	time = models.IntegerField(help_text="Duration of the quiz in minutes")
	required_score_to_pass = models.IntegerField(help_text="Required score in %")
	difficulty = models.CharField(max_length=6,choices=DIFF_CHOICES)
	created = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return f'{self.name}-{self.topic}'

	def get_questions(self):
		questions = list(self.question_set.all())
		random.shuffle(questions)
		return questions[:self.number_of_questions]

	class Meta:
		verbose_name_plural = "Quizes"
