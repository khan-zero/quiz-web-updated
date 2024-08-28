from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

from . import models

from random import choice, sample
from colorama import Fore, init


init(autoreset=True)

#def index(request):
#    return render(request, 'index.html')


def quizList(request):
    images = [
        'https://st2.depositphotos.com/2769299/7314/i/450/depositphotos_73146775-stock-photo-a-stack-of-books-on.jpg',
        'https://img.freepik.com/free-photo/creative-composition-world-book-day_23-2148883765.jpg',
        'https://profit.pakistantoday.com.pk/wp-content/uploads/2018/04/Stack-of-books-great-education.jpg',
        'https://live-production.wcms.abc-cdn.net.au/73419a11ea13b52c6bd9c0a69c10964e?impolicy=wcms_crop_resize&cropH=1080&cropW=1918&xPos=1&yPos=0&width=862&height=485',
        'https://live-production.wcms.abc-cdn.net.au/398836216839841241467590824c5cf1?impolicy=wcms_crop_resize&cropH=2813&cropW=5000&xPos=0&yPos=0&width=862&height=485',
        'https://images.theconversation.com/files/45159/original/rptgtpxd-1396254731.jpg?ixlib=rb-4.1.0&q=45&auto=format&w=1356&h=668&fit=crop'
    ]
    
    quizes = models.Quiz.objects.filter(author=request.user)
    # images = sample(len(quizes), images)

    quizes_list = []

    for quiz in quizes:
        quiz.img = choice(images)
        quizes_list.append(quiz)
        print(Fore.RED + str(f"taht: {quiz.img}"))

        
    
    print(Fore.YELLOW + str(f"taht: {quizes_list[0].img}"))
    
    return render(request, 'quiz-list.html', {'quizzes':quizes_list})


def quizDetail(request, id):
    quiz = models.Quiz.objects.get(id=id)
    users = User.objects.count()
    return render(request, 'quiz-detail.html', {'quiz':quiz, 'users':users})
    

def opinionDetail(request, id):
    question = models.Question.objects.get(id=id)
    opinions = question.options 
    
    print(Fore.RED + str(f"manovi: {question.quiz} time: {timezone.now()}"))
    
    return render(request, 'opinion-detail.html', {'question': question, 'opinions': opinions})
    

def deleteOption(request, id):
    option = get_object_or_404(models.Option, id=id)
    question_id = option.question.id
    option.delete()
    return redirect('opinionDetail', id=question_id)
        
        
def createQuiz(request):
    if request.method == 'POST':
        quiz = models.Quiz.objects.create(
            name = request.POST['name'],
            amount = request.POST['amount'],
            author = request.user
        )
        return redirect('quizDetail', quiz.id)
    return render(request, 'quiz-create.html')


def createQuestion(request, id):
    if request.method == 'POST':
    
        quiz = models.Quiz.objects.get(id=id)
        author = request.user
        start_time = timezone.now()
        
        question_text = request.POST.get('quiz')
        answers = request.POST.getlist('answer')
        
        #print(Fore.YELLOW + str(f"this: {quiz}"))
        #print(Fore.YELLOW + str(f"this: {author}"))
        #print(Fore.YELLOW + str(f"this: {start_time}"))
        #print()
        #print(Fore.YELLOW + str(f"this: {question_text}"))
        #print(Fore.YELLOW + str(f"this: {answers}"))
        
        answer = models.Answer.objects.create(
            quiz = quiz,
            author = author,
            start_time = start_time,
            end_time = timezone.now(),
            is_late = start_time + end_time == quiz.ammount
        )
        
        print(Fore.RED + str(f"this thing: {start_time}"))
        print(Fore.RED + str(f"this thing: {end_time}"))
        print(Fore.RED + str(f"this thing: {start_time + end_time}"))
        print(Fore.RED + str(f"this thing: {is_late}"))

        return redirect('createQuiz')

    else:
        return render(request, 'question-create.html', {})
        
        
def deleteQuestion(request, id):
    question = get_object_or_404(models.Question, id=id)
    quiz_id = question.quiz.id
    question.delete()
    return redirect('quizDetail', id=quiz_id)
