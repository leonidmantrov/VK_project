from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from .models import User


def registration_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.create_user(
                login=form.cleaned_data['login'],
                email=form.cleaned_data['email'],
                nickname=form.cleaned_data['nickname'],
                password=form.cleaned_data['password']
            )

            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
                user.save()

            login(request, user)
            return redirect('questions:questions_page')

        return render(request, 'acc/registration.html', {
            'form': form,
            'login_error': form.errors.get('login'),
            'email_error': form.errors.get('email'),
            'password_error': form.errors.get('__all__'),
            'user_login': request.POST.get('login', ''),
            'user_email': request.POST.get('email', ''),
            'user_nickname': request.POST.get('nickname', ''),
        })

    return render(request, 'acc/registration.html')


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            login_value = form.cleaned_data['login']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(login=login_value)
            except User.DoesNotExist:
                return render(request, 'acc/login.html', {
                    'login_error': 'Пользователь с таким логином не найден',
                    'user_login': login_value,
                })

            if user.check_password(password):
                login(request, user)
                return redirect('questions:questions_page')
            else:
                return render(request, 'acc/login.html', {
                    'password_error': 'Неверный пароль',
                    'user_login': login_value,
                })

        return render(request, 'acc/login.html', {
            'login_error': form.errors.get('login'),
            'password_error': form.errors.get('password'),
            'user_login': request.POST.get('login', ''),
        })

    return render(request, 'acc/login.html')


def settings_page(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login_page')

    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.nickname = request.POST.get('nickname', user.nickname)

        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('password', '')

        if new_password:
            if not user.check_password(old_password):
                return render(request, 'acc/settings.html', {
                    'user': user,
                    'password_error': 'Старый пароль неверен',
                })
            user.set_password(new_password)

        user.save()
        if new_password:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)

        return redirect('accounts:settings_page')

    return render(request, 'acc/settings.html', {
        'user': request.user,
        'user_login': request.user.login,
        'user_email': request.user.email,
        'user_nickname': request.user.nickname,
    })


def logout_page(request):
    logout(request)
    return redirect('questions:questions_page')