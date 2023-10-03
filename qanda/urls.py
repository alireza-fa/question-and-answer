from django.urls import path

from . import views


app_name = 'qanda'

urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('categories/questions/', views.CategoryQuestionListView.as_view()),
    path('questions/', views.QuestionLineView.as_view()),
    path('questions/create/', views.QuestionCreateView.as_view()),
    path('questions/answers/', views.QuestionAnswerListView.as_view()),
    path('questions/like/', views.QuestionLineView.as_view()),
    path('questions/dislike/', views.QuestionDislikeView.as_view()),
    path('questions/save/', views.QuestionSaveView.as_view()),
    path('answers/create/', views.AnswerCreateView.as_view()),
    path('answers/like/', views.AnswerLikeView.as_view()),
    path('answers/dislike/', views.AnswerDislikeView.as_view()),
    path('answers/save/', views.AnswerSaveView.as_view()),
]
