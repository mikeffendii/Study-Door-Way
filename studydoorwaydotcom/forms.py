from django import forms
from django.forms import ModelForm
from accounts.models import UserProfile



class RegisterAsTeacher(ModelForm):
	class Meta:
		model = UserProfile
		fields = ['', '']