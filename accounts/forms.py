from django import forms
from .models import *
from validate_email import validate_email
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from django.contrib.auth import (
	authenticate,
	get_user_model,
) 

User = get_user_model()


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError('Invalid username')
			if not user.check_password(password):
				raise forms.ValidationError('Invalid password')
			if not user.is_active:
				raise forms.ValidationError('User is not active')
		return super(UserLoginForm,self).clean(*args, **kwargs)	
		
class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email Address')
	email2 = forms.EmailField(label='Confirm Email') 
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
			'first_name',
			'last_name',
		]

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Emails must match")	
		email_qs = 	User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email is already being used")
		
		return super(UserRegisterForm,self).clean(*args, **kwargs)	

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		widgets = {
		'phone': PhoneNumberPrefixWidget(initial='PK'),
		'address':forms.Textarea(attrs={'rows':2}),
		'bio':forms.Textarea(attrs={'rows':3}),
        }
		fields = '__all__'
		exclude = ['user','role']
		
class TeacherProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
		]

class RegisterAsTeacherForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		widgets = {
		'phone': PhoneNumberPrefixWidget(initial='PK'),
        }
		fields = [
			'phone',
			'role',
		]			
				

# class ProfileUpdateForm(forms.ModelForm):
# 	class Meta:
# 		model = Profile
# 		fields = ['image']

