from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField



class UserProfile(models.Model):
	phone = PhoneNumberField(null=True, blank=True)
	address = models.TextField(null=True,blank=True)
	role_choice = (('Lecturer', 'Lecturer'),('Student', 'Student'))
	role = models.CharField(max_length=100,choices=role_choice,default='Lecturer')
	user = models.OneToOneField(User,null=True,on_delete=models.CASCADE,default='')
	bio = models.TextField(null=True,blank=True)
	profile_pic = models.ImageField(null=True,blank=True,default='profile pic.jpg',upload_to='profiles/')
	website_url = models.URLField(max_length=150,blank=True,null=True)
	facebook_url = models.URLField(max_length=150,blank=True,null=True)
	twitter_url = models.URLField(max_length=150,blank=True,null=True)
	github_url = models.URLField(max_length=150,blank=True,null=True)
	instagram_url = models.URLField(max_length=150,blank=True,null=True)
	youtube_url = models.URLField(max_length=150,blank=True,null=True)

# default='studydoorway_logo.png'
	def __str__(self):
		return str(self.user)


