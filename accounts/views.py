from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm, SettingsForm
from .models import User
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages

def registration_page(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('questions:questions_page')
        else:
            print("Ошибки формы:", form.errors)

        return render(request, 'acc/registration.html', {'form': form})

    form = RegistrationForm()
    return render(request, 'acc/registration.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)

            next_url = request.GET.get('next')
            if next_url:
                # редирект только на разрешенные хосты
                if url_has_allowed_host_and_scheme(
                        url=next_url,
                        allowed_hosts={request.get_host()},  # текущий хост
                        require_https=request.is_secure()
                ):
                    return redirect(next_url)
            return redirect('questions:questions_page')

        return render(request, 'acc/login.html', {
            'form': form,
            'user_login': request.POST.get('login', ''),
        })

    form = LoginForm()
    return render(request, 'acc/login.html', {'form': form})

def settings_page(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login_page')

    user = request.user

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=user, user=user)

        if form.is_valid():
            user = form.save()
            # Обновляем сессию, если пароль был изменен
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            messages.success(request, 'Настройки успешно сохранены!')
            return redirect('accounts:settings_page')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = SettingsForm(instance=user, user=user)

    return render(request, 'acc/settings.html', {
        'form': form,
        'user': user
    })

def logout_page(request):
    logout(request)
    return redirect('questions:questions_page')