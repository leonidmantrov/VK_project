from django.shortcuts import render


def login_page(request):
    return render(request, 'acc/login.html')


def settings_page(request):
    return render(request, 'acc/settings.html')


def registration_page(request):
    return render(request, 'acc/registration.html')