from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from .models import *
from accounts.models import *
from django.views.generic.detail import DetailView
from quizes.models import Quiz
from results.models import Result
import datetime
from django.http import JsonResponse


# Generate a PDF file Students Grades


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_pdf_view(request,class_id,s_id):
	template_path = 'classes/DMC_Test.xhtml'
	student = Student.objects.get(id=s_id)
	class_room = ClassRoom.objects.get(id=class_id)
	students = Student.objects.filter(class_room=class_room)
	assignments = Assignment.objects.filter(class_room=class_room)
	quizes = Quiz.objects.filter(class_room=class_room)
	mid_final_marks = MidFinalMarks.objects.get(class_room=class_room,student=student)

	total_quizes_points = Quiz.objects.filter(class_room=class_room).count()*100

	passed_quizes = 0
	failed_quizes = 0
	for q in Quiz.objects.filter(class_room=class_room):
		if Result.objects.filter(quiz=q,student=student).exists():
			obtained_quizes_points = Result.objects.get(quiz=q,student=student).score
			if obtained_quizes_points >= q.required_score_to_pass:
				passed_quizes +=100
			else:
				failed_quizes -=100
		else:
			pass
	if passed_quizes < 0:
		passed_quizes = 0
	elif failed_quizes < 0 :
		failed_quizes = 0

	obtained_quizes_points = passed_quizes-failed_quizes
	

	obtained_assignments_points = 0
	for sub in student.submission_set.all():
	 	obtained_assignments_points += sub.grade

	total_assignments_points = 0
	for ap in assignments:
	 	total_assignments_points += ap.points


	assignment_per = (obtained_assignments_points/total_assignments_points)*10
	quizes_per = (obtained_quizes_points/total_quizes_points)*10
	mid_per = (mid_final_marks.mid_marks/mid_final_marks.mid_marks_out_of)*20
	final_per = (mid_final_marks.final_marks/mid_final_marks.final_marks_out_of)*60
	total_per = assignment_per+quizes_per+mid_per+final_per

	context = {
		'student':student,
		'class':class_room,
		'total_per':total_per,
		'ass_per':assignment_per,
		'quiz_per':quizes_per,
		'mid_per':mid_per,
		'final_per':final_per,
		'students':students,
		'assignments':assignments,
		'quizes':quizes,
	}
	 # Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="Student Report.pdf"'
	 # find the template and render it.
	template = get_template(template_path)
	html = template.render(context)

	 # create a pdf
	pisa_status = pisa.CreatePDF(
	   html, dest=response)
	 # if error then show some funy view
	if pisa_status.err:
	   return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response


 
@login_required
def create_class_view(request):
	form = CreateClassRoom()
	join_class_form = JoinClassRoom()
	classes_created = ClassRoom.objects.filter(user=request.user)
	student = Student.objects.filter(student=request.user)
	notifications = Notification.objects.filter(viewed=False)
	
	classes_joined = [] 
	
	for student_info in student:
		classes_joined.append(student_info.class_room)



	if request.method == 'POST':
		if 'create_classroom' in request.POST:
			form = CreateClassRoom(request.POST,request.FILES)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = request.user
				instance.save()
				classroom = ClassRoom.objects.get(id=instance.id)
				messages.success(request,'Classrooom created successfully')
				return redirect('/classes/create_class/')
			else:
				messages.warning(request,'Error! Classroom not created Please correct the error in the form')
		if 'join_classroom' in request.POST:
			join_class_form = JoinClassRoom(request.POST)
			if join_class_form.is_valid():
				student_key = request.POST.get('student_key')
				class_room = ClassRoom.objects.get(student_key=student_key)
				student = request.user
				if Student.objects.filter(student=student,class_room=class_room).exists():
					messages.warning(request,'you are already a student in this classroom  '+ class_room.class_name)
				elif Instructor.objects.filter(instructor=student,class_room=class_room).exists():
					messages.warning(request,'you are the creator of this class [' + class_room.class_name + '] you can not join this class as student')
				else:					
					new_student = Student(student=student,class_room=class_room)
					new_student.save()
					print(new_student)
					messages.success(request,'Classrooom joined successfully')
					return redirect('/classes/create_class/')

	context = {
		'form': form,
		'join_class_form': join_class_form,
		'classes_created': classes_created,
		'classes_joined': classes_joined,
		'notifications': notifications,
	}
	
	return render(request,'classes/create_class.html',context)


@login_required
def announcement_likes_view(request,pk,class_id):
	student = request.user
	class_room = ClassRoom.objects.get(id=class_id)
	announcement = get_object_or_404(Announcement, id=request.POST.get('announcement_id'))
	
	if announcement.likes.filter(id=request.user.id).exists():
		announcement.likes.remove(request.user)
	else:	
		announcement.likes.add(request.user)

	if Student.objects.filter(student=student,class_room=class_room).exists():
		return HttpResponseRedirect(reverse('s_class_info', args=[str(class_id)]))


	return HttpResponseRedirect(reverse('class_info', args=[str(class_id)]))



@login_required
def announcement_comments_view(request,announcement_id,class_id):
	student = request.user
	class_room = ClassRoom.objects.get(id=class_id) 
	announcement = Announcement.objects.get(id=announcement_id)
	if request.method == 'POST':
		comment_text = request.POST.get('comment_text')
		Comment.objects.create(user=request.user,announcement=announcement,comment_text=comment_text)

		if Student.objects.filter(student=student,class_room=class_room).exists():
			return HttpResponseRedirect(reverse('s_class_info', args=[str(class_id)]))		
	return HttpResponseRedirect(reverse('class_info', args=[str(class_id)]))



@login_required
def announcement_update_view(request,class_id,announcement_id):
	announcement = Announcement.objects.get(id=announcement_id)
	update_announcement_form = CreateAnnouncement(instance=announcement)
	if request.method == 'POST':
		update_announcement_form = CreateAnnouncement(request.POST,request.FILES,instance=announcement)
		if update_announcement_form.is_valid():
			update_announcement_form.save()
			messages.success(request, 'Announcement updated successfully')
			return redirect('class_info',id=class_id)

	context = {
		'update_announcement_form': update_announcement_form,
		'announcement':announcement,
	}
	return render(request,'classes/update_announcement.html',context)


@login_required
def announcement_delete_view(request,class_id,announcement_id):
	announcement = Announcement.objects.get(id=announcement_id)
	if request.method == 'POST':
		announcement.delete()
		messages.warning(request, 'Announcement deleted successfully')
		return redirect('class_info',id=class_id)

	context = {
		'announcement':announcement,
	}
	return render(request,'classes/delete_announcement.html',context)

@login_required
def class_info_view(request,id):
	student = request.user
	classes_created = ClassRoom.objects.filter(user=request.user)
	student_classes = Student.objects.filter(student=request.user)
	classes_joined = []
	for student_info in student_classes:
		classes_joined.append(student_info.class_room)


	classroom = ClassRoom.objects.get(id=id)
	assignments = Assignment.objects.filter(class_room = id)
	if 's' in request.GET:
		s = request.GET['s']
		students = Student.objects.filter(student__first_name__icontains = s)

		if not students:
			messages.warning(request,'Student not found')
	else:
		students = Student.objects.filter(class_room=classroom)
	instructors = Instructor.objects.filter(class_room=classroom)
	quizes = Quiz.objects.filter(class_room=classroom)
	lectures = Lecture.objects.filter(class_room=classroom).order_by('-upload_date')



	
	create_class_form = CreateClassRoom(instance=classroom)
	create_assignment_form = CreateAssignment()
	create_announcement_form = CreateAnnouncement()
	create_quiz_form = CreateQuiz()


	announcements = Announcement.objects.filter(class_room=classroom).order_by('-announcement_date')
	if request.method == 'POST':

		if 'upload_lectures' in request.POST:
			lecture_title = request.POST.get('lecture_title')
			lecture_files = request.FILES.getlist('lecture_files')

			for f in lecture_files:
				Lecture.objects.create(title=lecture_title,files=f,class_room=classroom)

			messages.success(request,'Lectures uploaded successfully')
			return redirect('class_info',id=id)

		if 'announce' in request.POST:
			
			announcement_text = request.POST.get('announcement_text')
			announcement_file = request.FILES.get('announcement_file',None)
			if not announcement_file:
				Announcement.objects.create(announcement_text=announcement_text,user=request.user,class_room=classroom)
			else:
				# announcement_file = request.FILES['announcement_file']
				Announcement.objects.create(announcement_text=announcement_text,announcement_file=announcement_file,user=request.user,class_room=classroom)
			
			return redirect('class_info',id=id)
			
		if 'edit_class' in request.POST:
			create_class_form = EditClassRoom(request.POST, request.FILES, instance=classroom)
			if create_class_form.is_valid():
				create_class_form.save()
				messages.success(request,'classroom updated successfully')
				return redirect('class_info',id=id)
			else:
				messages.warning(request, create_class_form.errors)
		# if 'delete_class' in request.POST:
		# 	class_room = ClassRoom.objects.get(id=id)
		# 	class_room.delete()
		# 	messages.warning(request, 'Assignment deleted successfully')
		# 	return render(request,'classes/create_class.html')
		if 'create_assignment' in request.POST:
			create_assignment_form = CreateAssignment(request.POST, request.FILES)
			if create_assignment_form.is_valid():
				instance = create_assignment_form.save(commit=False)
				instance.user = request.user
				instance.class_room = classroom
				instance.save()
				messages.success(request,'Assignment created successfully')
				create_assignment_form = CreateAssignment()
				return redirect('class_info',id=id)
		if 'create_quiz' in request.POST:
			create_quiz_form = CreateQuiz(request.POST)
			if create_quiz_form.is_valid():
				instance = create_quiz_form.save(commit=False)
				instance.created_by = request.user
				instance.class_room = classroom
				instance.save()
				messages.success(request,'Assignment Quiz created successfully')
				return redirect('class_info',id=id)

	context = {
		'class':get_object_or_404(ClassRoom, pk=id),
		'assignments':assignments,
		'create_class_form':create_class_form,
		'create_assignment_form':create_assignment_form,
		'create_quiz_form':create_quiz_form,
		'students':students,
		'instructors':instructors,
		'classes_created':classes_created,
		'classes_joined':classes_joined,
		'announcements':announcements,
		'quizes':quizes,
		'lectures':lectures,
	}
	return render(request,'classes/class_info.html',context)


def add_final_marks_view(request,class_id,s_id):
	student = Student.objects.get(id=s_id)
	class_room = ClassRoom.objects.get(id=class_id)
	if MidFinalMarks.objects.filter(student=student,class_room=class_room).exists():
		midMarks = MidFinalMarks.objects.get(student=student,class_room=class_room) 
		mid_final_marks_form = MidFinalMarksForm(instance=midMarks)
	else:
		mid_final_marks_form = MidFinalMarksForm()

	if request.method == 'POST':
		if MidFinalMarks.objects.filter(student=student,class_room=class_room).exists():
			midFinal = MidFinalMarks.objects.get(student=student,class_room=class_room)
			mid_final_marks_form = MidFinalMarksForm(request.POST,instance=midFinal)
			if mid_final_marks_form.is_valid():
				mid_final_marks_form.save()
				messages.success(request,'Mid & Final marks submitted successfully for '+student.student.first_name)
		else:
			mid_final_marks_form = MidFinalMarksForm(request.POST)
			if mid_final_marks_form.is_valid():
				instance = mid_final_marks_form.save(commit=False)
				instance.student = student
				instance.class_room = class_room
				instance.save()
				messages.success(request,'Mid & Final marks submitted successfully for '+student.student.first_name)

	context = {
		'student':student,
		'form': mid_final_marks_form,
	}

	return render(request,'classes/final_marks.html',context)



from django.forms.formsets import formset_factory

def add_question_view(request,class_id,quiz_id):
	quiz = Quiz.objects.get(id=quiz_id)
	class_room = ClassRoom.objects.get(id=class_id)

	QuizAnswerFormSet = formset_factory(QuizAnswerForm, extra=2, min_num=2, validate_min=True)

	if request.method == 'POST':
		question_form = QuizQuestionForm(request.POST)
		formset = QuizAnswerFormSet(request.POST)
		if all([question_form.is_valid(), formset.is_valid()]):
			question = question_form.save()
			for inline_form in formset:
				if inline_form.cleaned_data:
					answer = inline_form.save(commit=False)
					answer.question = question
					answer.save()
			messages.success(request,'Question added to quiz successfully')
			return redirect('class_info', id=class_id)
	else:
		question_form = QuizQuestionForm()
		formset = QuizAnswerFormSet()
	context = {
		'question_form':question_form,
		'formset':formset,
	}
	return render(request,'classes/add_question.html',context)

@login_required
def student_work_view(request,class_id,assignment_id):
	class_room = ClassRoom.objects.get(id=class_id)
	assignment = Assignment.objects.get(id=assignment_id)
	submissions = assignment.submissions.all()
	ungraded_sub = assignment.submissions.filter(grade=000).count()
	grade_form = GradeForm(request.POST or None)
	feedback_form = FeedbackForm(request.POST or None)
	print(submissions)
	if request.method == 'POST':
		if 'submit-feedback' in request.POST:
			if feedback_form.is_valid():
				feedback = request.POST['feedback']
				submission_id = request.POST['submit-feedback']
				submission = Submission.objects.get(id=submission_id)
				submission.feedback = feedback
				submission.save()
				messages.success(request,'Feedback added successfully for '+submission.student.student.username)
				notification = Notification.objects.create(user=request.user,class_room=class_room,assignment=assignment,title='New Feedback')
				# return redirect('http://127.0.0.1:8000/classes/'+str(class_id)+'/'+str(assignment_id)+'/student_work')
		if 'submit-grade' in request.POST:
			if grade_form.is_valid():
				grade = request.POST['grade']
				grade = int(grade)
				if grade > assignment.points:
					messages.warning(request,'Max points for this assignment is '+ str(assignment.points))
				else:
					submission_id = request.POST['submit-grade']
					submission = Submission.objects.get(id=submission_id)
					submission.grade = grade
					submission.save()
					messages.success(request,"Submission graded successfully for "+submission.student.student.username)
					notification = Notification.objects.create(user=request.user,class_room=class_room,assignment=assignment,title='New Grade')
	context = {
		'class':get_object_or_404(ClassRoom, pk=class_id),
		'assignment':get_object_or_404(Assignment, pk=assignment_id),
		'submissions': submissions,
		"grade_form": grade_form,
		'feedback_form': feedback_form,
		'ungraded_sub':ungraded_sub,
		
	}
	return render(request,'classes/student_work.html',context)


@login_required
def s_class_info_view(request,id):
	assignments = Assignment.objects.filter(class_room = id)
	students = Student.objects.filter(class_room= id)
	instructors = Instructor.objects.filter(class_room= id)
	class_room = ClassRoom.objects.get(id=id)
	announcements = class_room.announcements.all().order_by('-announcement_date')
	quizes = Quiz.objects.filter(class_room=class_room)
	lectures = Lecture.objects.filter(class_room=class_room).order_by('-upload_date')


	student = Student.objects.get(student=request.user,class_room=class_room)
	# students = Student.objects.filter(class_room=class_room)
	mid_final_marks = MidFinalMarks.objects.get(class_room=class_room,student=student)

	total_quizes_points = Quiz.objects.filter(class_room=class_room).count()*100

	passed_quizes = 0
	failed_quizes = 0
	for q in Quiz.objects.filter(class_room=class_room):
		if Result.objects.filter(quiz=q,student=student).exists():
			obtained_quizes_points = Result.objects.get(quiz=q,student=student).score
			if obtained_quizes_points >= q.required_score_to_pass:
				passed_quizes +=100
			else:
				failed_quizes -=100
		else:
			pass
	if passed_quizes < 0:
		passed_quizes = 0
	elif failed_quizes < 0 :
		failed_quizes = 0

	obtained_quizes_points = passed_quizes-failed_quizes
	

	obtained_assignments_points = 0
	for sub in student.submission_set.all():
	 	obtained_assignments_points += sub.grade

	total_assignments_points = 0
	for ap in assignments:
	 	total_assignments_points += ap.points


	assignment_per = (obtained_assignments_points/total_assignments_points)*100
	quizes_per = (obtained_quizes_points/total_quizes_points)*100
	mid_per = (mid_final_marks.mid_marks/mid_final_marks.mid_marks_out_of)*100
	final_per = (mid_final_marks.final_marks/mid_final_marks.final_marks_out_of)*100
	total_per = ((obtained_assignments_points/total_assignments_points)*10)+((obtained_quizes_points/total_quizes_points)*10)+((mid_final_marks.mid_marks/mid_final_marks.mid_marks_out_of)*20)+((mid_final_marks.final_marks/mid_final_marks.final_marks_out_of)*60)

	if total_per >=80:
		grade = 'A'
	elif total_per >=75:
		grade = 'B+'
	elif total_per >=70:
		grade = 'B'
	elif total_per >=65:
		grade = 'C+'
	elif total_per >=60:
		grade = 'C'
	elif total_per <60:
		grade = 'F'



	context = {
		'class':get_object_or_404(ClassRoom, pk=id),
		'assignments':assignments,
		'quizes':quizes,
		'instructors':instructors,
		'students':students,
		'announcements':announcements,
		'lectures':lectures,

		'assignment_per':assignment_per,
		'quizes_per':quizes_per,
		'mid_per':mid_per,
		'final_per':final_per,
		'total_per':total_per,
		'grade':grade,

	}
	return render(request, 'classes/s_class_info.html',context)

@login_required
def update_assignment_view(request,class_id,assignment_id):
	assignment = Assignment.objects.get(id=assignment_id)
	update_assignment_form = CreateAssignment(instance=assignment)
	if request.method == 'POST':
		update_assignment_form = CreateAssignment(request.POST,request.FILES,instance=assignment)
		if update_assignment_form.is_valid():
			update_assignment_form.save()
			messages.success(request, 'Assignment updated successfully')
			return redirect('class_info',id=class_id)

	context = {
		'update_assignment_form': update_assignment_form,
		'assignment':assignment,
	}		
	return render(request,'classes/update_assignment.html',context)


@login_required
def delete_assignment_view(request,class_id,assignment_id):
	assignment = Assignment.objects.get(id=assignment_id)
	if request.method == 'POST':
		assignment.delete()
		messages.warning(request, 'Assignment deleted successfully')
		return redirect('class_info',id=class_id)

	context = {
		'assignment':assignment,
	}
	return render(request,'classes/delete_assignment.html',context)


@login_required
def delete_notification_view(request,notification_id):
	notification = Notification.objects.get(id=notification_id)
	notification.viewed = True
	notification.delete()
	return redirect('create_class')



@login_required
def s_assignment_detail_view(request,class_id,assignment_id):
	classroom = ClassRoom.objects.get(id=class_id)
	assignment = Assignment.objects.get(id=assignment_id)
	submission_form = SubmitAssignment()
	student = Student.objects.get(student=request.user,class_room=classroom)
	
	if Submission.objects.filter(student=student,assignment=assignment).exists():
		s_submission = Submission.objects.get(student=student,assignment=assignment)
		submission_form = SubmitAssignment(instance=s_submission)
	else:
		s_submission = ''

	if request.method == 'POST':
		if 'submit_assignment' in request.POST:
			submission_form = SubmitAssignment(request.POST,request.FILES)
			if submission_form.is_valid():
				instance = submission_form.save(commit=False)
				instance.student = student
				instance.assignment = Assignment.objects.get(id=assignment_id)
				instance.save()
				messages.success(request, 'Assignment submitted successfully')
				return redirect('s_class_info',id=class_id)
		if 'resubmit_assignment' in request.POST:
			submission_form = SubmitAssignment(request.POST,request.FILES,instance=s_submission)
			if submission_form.is_valid():
				submission_form.save()
				s_submission.last_updated = datetime.datetime.now()
				s_submission.save()
				messages.success(request, 'Assignment edited successfully')

	context = {
		'assignment': assignment,
		'submission_form': submission_form,
		's_submission' : s_submission,
	}
	return render(request,'classes/s_assignment_detail.html',context)


@login_required
def attendance_view(request,class_id):
	class_room = ClassRoom.objects.get(id=class_id)
	students = Student.objects.filter(class_room=class_room)
	attendanceForm = AttendanceForm()
	attendances = Attendance.objects.filter(class_room=class_room)
	
	if request.method == 'POST':
		if 'submit-date' in request.POST:
			attendanceForm = AttendanceForm(request.POST)
			if attendanceForm.is_valid():
				created_at = request.POST.get('created_at')
				if Attendance.objects.filter(created_at=created_at).exists():
					messages.warning(request,'You have already submitted attendance for this date')

	if request.is_ajax() and request.method == 'POST':
		created_at = request.POST.get('attDate')
		present_ids = request.POST.getlist('p_ids[]')
		absent_ids = request.POST.getlist('a_ids[]')

		for pid in present_ids:
			student = Student.objects.get(pk=pid)
			Attendance.objects.create(student=student,attendance='P',class_room=class_room,created_at=created_at)
		for aid in absent_ids:
			student = Student.objects.get(pk=aid)
			Attendance.objects.create(student=student,attendance='A',class_room=class_room,created_at=created_at)

		messages.success(request,'Attendance submitted successfully')
		# ps = Attendance.objects.filter(present=True)
		# present_s = []
		# for pr_s in ps:
		# 	present_s.append((pr_s.student.student.first_name, pr_s.present,pr_s.created_at))
		# return JsonResponse({
		# 	'attendance':list(present_s),
		# })
			
		

	context = {
		'students':students,
		'attendanceForm':attendanceForm,
		'class_room':class_room,
	}
	return render(request,'classes/attendance.html',context)


@login_required
def view_attendance(request,class_id):
	class_room = ClassRoom.objects.get(id=class_id)
	if request.method=="POST":
		attendance_date = request.POST.get('attendance_date')
		sResult = Attendance.objects.filter(class_room=class_room,created_at=attendance_date)
		return render(request,'classes/view_attendance.html',{"data":sResult,"class_room":class_room})
	else:
		attendances = Attendance.objects.filter(class_room=class_room)
		return render(request,'classes/view_attendance.html',{"data":attendances,"class_room":class_room})


@login_required
def edit_attendance(request,class_id,att_id):
	class_room = ClassRoom.objects.get(id=class_id)
	attendance = Attendance.objects.get(id=att_id)
	edit_att_form = EditAttendanceForm(instance=attendance)
	if request.method == 'POST':
		edit_att_form = EditAttendanceForm(request.POST,instance=attendance)
		if edit_att_form.is_valid():
			edit_att_form.save()
			messages.success(request, 'Attendance edited successfully')
			return redirect('http://127.0.0.1:8000/classes/class_info/'+str(class_id)+'/view_attendance')

	return render(request,'classes/edit_attendance.html',{'edit_att_form':edit_att_form,'attendance':attendance,'class_room':class_room})



import xlwt
from django.http import HttpResponse




@login_required
def export_attendance_xls(request,class_id):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'filename="Attendance.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Attendance Data') # this will make a sheet named Attendance Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    class_room = ClassRoom.objects.get(id=class_id)
    attendances = Attendance.objects.filter(class_room=class_room)
    att_dates = []
    for att in attendances:
    	att_dates.append(att.created_at)
    columns = ['Student Name','Date','Attendance']


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # for col_num in range(len(att_dates)):
    # 	ws.write(row_num, col_num, att_dates[col_num], font_style)
    # students = Student.objects.filter(class_room=class_room)

    # attendances= Attendance.objects.filter(class_room=class_room)
    # att=[]
    # for a in attendances:
    # 	att.append(a.created_at)

    # att= list(set(att))
   



    # context = {
    # 	'students':students,
    # 	'att':att,
    # }

    # return render(request,'classes/example.html',context)



    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Attendance.objects.filter(class_room=class_room)
    rows = rows.extra(select={'datestr':"to_char(created_at, 'YYYY-MM-DD')"})
    rows = rows.values_list('student__student__first_name', 'datestr','attendance')
    

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response


def rate(request,class_id):
	class_room = ClassRoom.objects.get(id=class_id)
	user = request.user
	reviews = Review.objects.filter(class_room=class_room)

	total_reviews = reviews.count()
	master_piece = (Review.objects.filter(class_room=class_room,rate=10).count()/total_reviews)*100
	perfect = (Review.objects.filter(class_room=class_room,rate=9).count()/total_reviews)*100
	very_good = (Review.objects.filter(class_room=class_room,rate=8).count()/total_reviews)*100
	good = (Review.objects.filter(class_room=class_room,rate=7).count()/total_reviews)*100
	understandable = (Review.objects.filter(class_room=class_room,rate=6).count()/total_reviews)*100
	ok = (Review.objects.filter(class_room=class_room,rate=5).count()/total_reviews)*100
	bad = (Review.objects.filter(class_room=class_room,rate=4).count()/total_reviews)*100
	terible = (Review.objects.filter(class_room=class_room,rate=3).count()/total_reviews)*100
	horible = (Review.objects.filter(class_room=class_room,rate=2).count()/total_reviews)*100
	trash = (Review.objects.filter(class_room=class_room,rate=1).count()/total_reviews)*100

	if request.method == 'POST':
		form = RateForm(request.POST)
		if form.is_valid():
			rate = form.save(commit=False)
			rate.user = user
			rate.class_room = class_room
			rate.save()
			messages.success(request, 'Review added successfully')
			return HttpResponseRedirect(reverse('s_class_info', args=[class_id]))
	else:
		form = RateForm()

	context = {
		'form':form,
		'class':class_room,
		'reviews':reviews,
		'master_piece':master_piece,
		'perfect':perfect,
		'very_good':very_good,
		'good':good,
		'understandable':understandable,
		'ok':ok,
		'bad':bad,
		'terible':terible,
		'horible':horible,
	}

	return render(request,'classes/rate.html',context)