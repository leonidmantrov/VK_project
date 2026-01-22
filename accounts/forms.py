from django import forms
from django.contrib.auth.hashers import check_password
from accounts.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Пароль')
    password_repeat = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = User
        fields = ['login', 'email', 'nickname', 'avatar']
        labels = {
            'login': 'Логин',
            'email': 'Email',
            'nickname': 'Никнейм',
            'avatar': 'Аватар'
        }

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

    def clean(self):
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user



class SettingsForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='Старый пароль'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='Новый пароль',
        min_length=8
    )
    new_password_repeat = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='Повторите новый пароль'
    )

    class Meta:
        model = User
        fields = ['email', 'nickname', 'avatar']
        labels = {
            'email': 'Email',
            'nickname': 'Никнейм',
            'avatar': 'Аватар'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['email'].initial = self.instance.email
            self.fields['nickname'].initial = self.instance.nickname

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            try:
                validate_password(new_password, self.user)
            except forms.ValidationError as e:
                raise forms.ValidationError(list(e.messages))
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password_repeat = cleaned_data.get('new_password_repeat')
        old_password = cleaned_data.get('old_password')

        if new_password:
            if not old_password:
                raise forms.ValidationError({
                    'old_password': 'Для смены пароля введите старый пароль'
                })

            if not self.user.check_password(old_password):
                raise forms.ValidationError({
                    'old_password': 'Старый пароль неверен'
                })
            if new_password != new_password_repeat:
                raise forms.ValidationError({
                    'new_password_repeat': 'Новые пароли не совпадают'
                })

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')

        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    login = forms.CharField(max_length=30, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if login and password:
            user = authenticate(username=login, password=password)

            if user is None:
                raise forms.ValidationError('Неверный логин или пароль')

            if not user.is_active:
                raise forms.ValidationError('Аккаунт деактивирован')

            cleaned_data['user'] = user

        return cleaned_data