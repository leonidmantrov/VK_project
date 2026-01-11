from django.urls import path
from questions import views

urlpatterns = [
    path('', views.questions_page, name='questions_page'),
    path('answer_for_question/<int:id>/', views.answers_page_for_question, name='answers_page_for_question'),
    path('questions/tag_search/', views.questions_by_tag, name='questions_by_tag'),
    path('addquestion/', views.add_question, name='add_question'),
    path('profile_member/<int:id>/', views.profile_member, name='profile_member'),
]