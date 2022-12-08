from django.shortcuts import render,redirect
from django.contrib.sessions.models import Session
from django.contrib import messages
from .models import *

from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
) 

from .forms import *

def login_view(request):
	next = request.GET.get('next')
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request,user)
		messages.success(request,'loged-in successfully!')
		if next:
			return redirect(next)

		request.session['is_loged'] = True	
		return redirect('/')
	

	context = {
		'form':form,
	}
	return render(request, 'accounts/login.html',context)		



def register_view(request):
	next = request.GET.get('next')
	form = UserRegisterForm(request.POST or None)
	
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)

		if next:
			return redirect(next)
		return redirect('/')
	

	context = {
		'form':form,
	}
	return render(request, 'accounts/signup.html',context)		



def logout_view(request):
	if request.method =="POST":
		logout(request)
		messages.success(request,'loged-out successfully')
		return redirect('/')
	return render(request,'accounts/logout.html') 	

def userprofile_view(request,profile_id):
	user_profile = UserProfile.objects.get(id=profile_id)
	update_form = UserProfileForm(instance=user_profile)
	if request.method =='POST':
		update_form = UserProfileForm(request.POST,request.FILES,instance=user_profile)
		if update_form.is_valid():
			update_form.save()
			messages.success(request,'Userprofile updated successfully')
			# return redirect('userprofile',id=profile_id)
		# messages.success(request,'Error! Userprofile not updated')
	
	context = {'update_form':update_form,'user_profile':user_profile}	
	return render(request,'accounts/userprofile.html',context)


def register_as_teacher_view(request,prof_id):
	user = request.user
	user_profile = UserProfile.objects.get(id=prof_id)
	teacher_profile_form = TeacherProfileForm(instance=user)
	reg_as_teacher_form = RegisterAsTeacherForm(instance=user_profile)
	if request.method == 'POST':
		teacher_profile_form = TeacherProfileForm(request.POST,instance=user)
		reg_as_teacher_form = RegisterAsTeacherForm(request.POST,request.FILES,instance=user_profile)
		if teacher_profile_form.is_valid() and reg_as_teacher_form.is_valid():
			teacher_profile_form.save()
			reg_as_teacher_form.save()
			messages.success(request,'User role has been updated successfully ')
			return redirect('home')



	context = {'teacher_profile_form': teacher_profile_form,'reg_as_teacher_form': reg_as_teacher_form}
	return render(request,'accounts/register_as_teacher.html',context)