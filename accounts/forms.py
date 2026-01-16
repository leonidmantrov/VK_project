from django import forms
from django.contrib.auth.hashers import check_password
from .models import User

class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=30, label='Логин')
    email = forms.EmailField(label='Email')
    nickname = forms.CharField(max_length=30, label='Никнейм')
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Пароль')
    password_repeat = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')
    avatar = forms.ImageField(required=False, label='Аватар')

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(login=login).exists():
            raise forms.ValidationError('Этот логин уже занят')
        return login

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email

    avatar = forms.ImageField(required=False, label='Аватар')
    def clean(self):
        """Валидация всех полей"""
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError('Пароли не совпадают')

        avatar = cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('Файл слишком большой (макс. 5MB)')

            ext = avatar.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                raise forms.ValidationError('Разрешены только JPG, PNG, GIF')

        return cleaned_data


class LoginForm(forms.Form):
    login = forms.CharField(max_length=30, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')