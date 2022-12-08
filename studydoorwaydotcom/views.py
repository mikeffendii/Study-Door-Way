from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from classes.models import ClassRoom
from django.contrib.auth.models import User
from classes.models import Student,Instructor,Notification

@login_required
def home(request):
	notifications = Notification.objects.filter(user=request.user)
	users = User.objects.all()
	students = Student.objects.all()
	instructors = Instructor.objects.all()
	students = students.count()
	instructors = instructors.count()
	users = users.count()
	classes = ClassRoom.objects.all()
	print(users,)
	context = {
		'classes':classes,
		'instructors':instructors,
		'students':students,
		'users':users,
		'notifications':notifications,
	}
	return render(request, 'home.html',context)

def about_us_view(request):
	return render(request, 'about_us.html')