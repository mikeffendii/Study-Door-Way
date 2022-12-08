from django import forms
from django.forms import ModelForm
from .models import *
from quizes.models import Quiz
from questions.models import Question,Answer
from django.contrib import admin


class RateForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)
	rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

	class Meta:
		model = Review
		fields = ('text', 'rate')

class DateInput(forms.DateInput):
	input_type = 'date'


class CreateClassRoom(ModelForm):
	student_key = forms.CharField(max_length=50,help_text='Enter the class joining key so students can use this key to enroll in this classroom')
	class Meta:
		model = ClassRoom
		fields = '__all__'
		exclude = ['user',]

	def clean_student_key(self):
		student_key = self.cleaned_data['student_key']
		if ClassRoom.objects.filter(student_key=student_key).exists():
			raise forms.ValidationError('Class room with this Student key already exists')
		return student_key

class EditClassRoom(ModelForm):
	class Meta:
		model = ClassRoom
		fields = '__all__'
		exclude = ['user',]
		

class CreateAssignment(ModelForm):
	class Meta:
		model = Assignment
		widgets = {'due_date' : DateInput()}
		fields = '__all__'
		exclude = ['user','class_room']

# class UploadLecture(ModelForm):
# 	class Meta:
# 		model = Lecture
# 		fields = '__all__'
# 		exclude = ['class_room']


class JoinClassRoom(forms.Form):
	student_key = forms.CharField(max_length=50,help_text='Enter the class joining key provided by class creator')


	def clean_student_key(self):
		student_key = self.cleaned_data['student_key']
		if not ClassRoom.objects.filter(student_key=student_key).exists():
			raise forms.ValidationError('No classroom exists with provided key')
		return student_key

class CreateAnnouncement(ModelForm):
	class Meta:
		model = Announcement
		fields = '__all__'
		exclude = ['user','class_room','likes']

# Quizes Forms 
class CreateQuiz(ModelForm):
	class Meta:
		model = Quiz
		fields = '__all__'
		exclude = ['created_by','class_room']

class QuizQuestionForm(ModelForm):
	text = forms.CharField(max_length=250,help_text='Enter question text here.')

	class Meta:
		model = Question
		fields = '__all__'

class QuizAnswerForm(ModelForm):
	text = forms.CharField(max_length=250,help_text='Enter answer text here.')
	class Meta:
		model = Answer
		fields = '__all__'
		exclude = ['question']


		
class SubmitAssignment(ModelForm):
	class Meta:
		model = Submission
		fields = ['file']

class GradeForm(forms.Form):
    grade = forms.IntegerField(help_text='Enter points obtained')

    class Meta:
        fields = ['grade']

class FeedbackForm(forms.Form):
    feedback = forms.CharField(help_text='Enter your feedback')
    
    class Meta:
        fields = ['feedback']

class AttendanceForm(ModelForm):
	created_at = models.DateField(help_text='Select date for attendance')
	class Meta:
		model = Attendance
		widgets = {'created_at' : DateInput()}
		fields = ['created_at']

	def clean_created_at(self):
		created_at = self.cleaned_data['created_at']
		if Attendance.objects.filter(created_at=created_at).exists():
			raise forms.ValidationError('You have already submitted attendance for this date')
		return created_at 

class EditAttendanceForm(ModelForm):
	class Meta:
		model = Attendance
		fields = ['attendance']


class MidFinalMarksForm(ModelForm):
	class Meta:
		model = MidFinalMarks
		fields = '__all__'
		exclude =['student','class_room']