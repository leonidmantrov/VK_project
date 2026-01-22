from django.urls import path
from questions import views
from . import ajax_views

app_name = 'questions'

urlpatterns = [
    path('', views.questions_page, name='questions_page'),
    path('answer_for_question/<int:id>/', views.answers_page_for_question, name='answers_page_for_question'),
    path('questions/tag_search/', views.questions_by_tag, name='questions_by_tag'),
    path('addquestion/', views.add_question, name='add_question'),
    path('profile_member/<int:id>/', views.profile_member, name='profile_member'),
    path('hot/', views.hot_questions_page, name='hot_questions_page'),

    path('ajax/vote/question_text/', ajax_views.vote_question, name='ajax_vote_question'),
    path('ajax/vote/answer/', ajax_views.vote_answer, name='ajax_vote_answer'),
    path('ajax/mark-correct/', ajax_views.mark_correct_answer, name='ajax_mark_correct'),
]