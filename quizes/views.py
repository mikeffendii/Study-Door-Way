from django.shortcuts import render
from classes.models import ClassRoom
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question,Answer
from results.models import Result
from classes.models import Student

class QuizListView(ListView):
	# class_room = ClassRoom.objects.get(id=class_id)
	# quizes = Quiz.objects.filter(class_room=class_room)
	# return render(request,'quizes/quizes_main.html',{'quizes':quizes})
	model = Quiz
	template_name = 'quizes/quizes_main.html'


def quiz_view(request,classId,pk):
	quiz = Quiz.objects.get(pk=pk)
	class_room = ClassRoom.objects.get(id=classId)
	student = Student.objects.get(student=request.user,class_room=class_room)
	if Result.objects.filter(quiz=quiz,student=student).exists():
		return render(request,'quizes/quiz_done.html')
	else:
		return render(request,'quizes/quiz.html',{'obj':quiz,'class_room':class_room})


def quiz_data_view(request,classId,pk):
	quiz = Quiz.objects.get(pk=pk)
	questions = []
	for q in quiz.get_questions():
		answers = []
		for a in q.get_answers():
			answers.append(a.text)
		questions.append({str(q):answers})
	return JsonResponse({
		'data':questions,
		'time':quiz.time,
	})

def save_quiz_view(request,classId,pk):
	# print(request.POST)
	if request.is_ajax():
		questions = []
		data = request.POST
		data_ = dict(data.lists())
		
		data_.pop('csrfmiddlewaretoken')
		
		for k in data_.keys():
			print('key:',k)
			question = Question.objects.get(text=k)
			questions.append(question)
		print(questions)


		class_room = ClassRoom.objects.get(id=classId)
		student = Student.objects.get(student=request.user,class_room=class_room)
		quiz = Quiz.objects.get(pk=pk)

		score = 0
		multiplier = 100/quiz.number_of_questions
		results = []
		correct_answer = None

		for q in questions:
			a_selected = request.POST.get(q.text)

			if a_selected != "":
				question_answers = Answer.objects.filter(question=q)
				for a in question_answers:
					if a_selected == a.text:
						if a.correct:
							score += 1
							correct_answer = a.text
					else:
						if a.correct:
							correct_answer = a.text
				
				results.append({str(q):{'correct_answer':correct_answer, 'answered':a_selected}})
			else:
				results.append({str(q):'not answered'})			
		
		score_ = score * multiplier
		Result.objects.create(quiz=quiz, student=student, score=score_, class_room=class_room)	

		if score_ >= quiz.required_score_to_pass:
			return JsonResponse({'passed':True, 'score':score_, 'results':results})
		else:
			return JsonResponse({'passed':False, 'score':score_, 'results':results})