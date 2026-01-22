from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from questions.models import Question, Answer
from django.conf import settings
from django.db.models import F, Sum
from django.db.models.functions import Coalesce


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
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'nickname']

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return f"{self.nickname} ({self.login})"

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url # self.avatar.url вернет /media/avatars/filename.jpg
        return f"{settings.STATIC_URL}img/avatarka.png"

    def update_rating(self, delta=None, recalc=False):
        if recalc:
            # Полный пересчёт (для инициализации)
            question_sum = Question.objects.filter(user=self
            ).aggregate(total=Coalesce(Sum('received_question_votes__vote_value'), 0))['total']

            answer_sum = Answer.objects.filter(user=self
            ).aggregate(total=Coalesce(Sum('received_answer_votes__vote_value'), 0))['total']

            new_rating = question_sum + answer_sum

            if self.rating != new_rating:
                self.rating = new_rating
                self.save(update_fields=['rating'])

            return new_rating

        elif delta is not None:
            User.objects.filter(id=self.id).update(rating=F('rating') + delta)
            self.refresh_from_db(fields=['rating'])
            return self.rating

        else:
            return self.rating