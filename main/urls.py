from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.quizList, name='quizList'),
    path('quiz-detail/<int:id>/', views.quizDetail, name='quizDetail'),
    path('opinion-detail/<int:id>/', views.opinionDetail, name='opinionDetail'),
    path('option/<int:id>/delete/', views.deleteOption, name='delete_option'),
    path('create-quiz', views.createQuiz, name='createQuiz'),
    path('create-question/<int:id>/', views.createQuestion, name='questionCreate'),
    path('delete-question/<int:id>/', views.deleteQuestion, name='delete-question'),
]
