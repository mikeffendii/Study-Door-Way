from django.forms import ModelForm
from django import forms
from .models import Answer,Question


class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ('detail',)

class QuestionForm(ModelForm):

	class Meta:
		widgets = {
		'tags':forms.Textarea(attrs={'rows':3}),
		}
		model = Question
		fields = ('title','detail','tags')
