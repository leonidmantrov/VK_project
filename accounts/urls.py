from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.registration_page, name='registration_page'),
    path('settings/', views.settings_page, name='settings_page'),
]