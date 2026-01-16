from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.registration_page, name='registration_page'),
    path('settings/', views.settings_page, name='settings_page'),
    path('logout/', views.logout_page, name='logout'),
]