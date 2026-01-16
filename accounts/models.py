# accounts/models.py (более простой вариант)
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, login, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not email:
            raise ValueError('Email обязателен')
        if not login:
            raise ValueError('Логин обязателен')

        email = self.normalize_email(email)
        user = self.model(login=login, email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, login, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(login, email, nickname, password, **extra_fields)


class User(AbstractUser):
    username = None

    login = models.CharField(max_length=255, unique=True, verbose_name='Логин')
    nickname = models.CharField(max_length=255, verbose_name='Никнейм')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'nickname']

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return f"{self.nickname} ({self.login})"