from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import Question,Answer,Comment,UpVote,DownVote
from django.http import JsonResponse
from .forms import AnswerForm,QuestionForm
from django.contrib import messages
from django.db.models import Count

# Internet Forum Homepage
def forum_homepage(request):
    
	if 'q' in request.GET:
		q=request.GET['q']
		quests = Question.objects.annotate(total_comments=Count('answer__comment')).filter(title__icontains=q).order_by('-id')
	else:
		quests = Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-id')
	paginator = Paginator(quests,4)
	page_num = request.GET.get('page',1)
	quests = paginator.page(page_num)

	return render(request,'internetforum/forum_home.html',{'quests':quests,'tags':tags})


# Detail
def detail(request,id):
	quest = Question.objects.get(pk=id)
	tags = quest.tags.split(',')
	answers = Answer.objects.filter(question=quest)
	answerform = AnswerForm
	if request.method =='POST':
		answerData = AnswerForm(request.POST)
		if answerData.is_valid():
			answer = answerData.save(commit=False)
			answer.question = quest
			answer.user = request.user
			answer.save()
			messages.success(request,'Answer has been submitted')
			return redirect('detail',id=id)
	context = {
		'quest':quest,
		'tags':tags,
		'answers':answers,
		'answerform':answerform		
	}
	return render(request,'internetforum/detail.html',context)


# Save Comment
def save_comment(request):
    if request.method=='POST':
        comment=request.POST['comment']
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        Comment.objects.create(
            answer=answer,
            comment=comment,
            user=user
        )
        return JsonResponse({'bool':True})


# Save Upvote
def save_upvote(request):
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=UpVote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            UpVote.objects.create(
                answer=answer,
                user=user,
            )
            return JsonResponse({'bool':True})

# Save Downvote
def save_downvote(request):
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=DownVote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            DownVote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})


# Ask Form
def ask_form(request):
    form=QuestionForm
    if request.method=='POST':
        questForm=QuestionForm(request.POST)
        if questForm.is_valid():
            questForm=questForm.save(commit=False)
            questForm.user=request.user
            questForm.save()
            messages.success(request,'Question has been added.')
            return redirect('ask-question')
    return render(request,'internetforum/ask-question.html',{'form':form})


# Questions according to tag
def tag(request,tag):
    quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(tags__icontains=tag).order_by('-id')
    paginator=Paginator(quests,10)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'internetforum/tag.html',{'quests':quests,'tag':tag})


# Tags Page
def tags(request):
    if 't' in request.GET:
        t=request.GET['t']
        quests = Question.objects.filter(title__icontains=t).order_by('-id')
        if not quests:
            messages.warning(request,'Tag not found!')
    else:
        quests=Question.objects.all()
    paginator = Paginator(quests,10)
    page_num = request.GET.get('page',1)
    quests = paginator.page(page_num)

    # quests=Question.objects.all()
    tags=[]
    for quest in quests:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    return render(request,'internetforum/tags.html',{'tags':tag_with_count,'quests':quests})

# Profile
def user_dashboard(request):
    quests=Question.objects.filter(user=request.user).order_by('-id')
    answers=Answer.objects.filter(user=request.user).order_by('-id')
    comments=Comment.objects.filter(user=request.user).order_by('-id')
    upvotes=UpVote.objects.filter(user=request.user).order_by('-id')
    downvotes=DownVote.objects.filter(user=request.user).order_by('-id')
    
    label = ['Questions', 'Upvotes', 'Downvotes','Answers','Comments']
    data = [quests.count(), upvotes.count(), downvotes.count(),answers.count(), comments.count()]
    return render(request,'internetforum/user-dashboard.html',{
        'quests':quests,
        'answers':answers,
        'comments':comments,
        'upvotes':upvotes,
        'downvotes':downvotes,
        'label':label,
        'data':data,
    })