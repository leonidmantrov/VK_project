from django.db import models
from django.utils import timezone
from accounts.models import User


class Tag(models.Model):
    id_t = models.AutoField(primary_key=True, db_column='id_t')
    tag = models.CharField(max_length=50, unique=True, db_column='tag')

    objects = models.Manager()
    class Meta:
        db_table = 'Tags'
        indexes = [
            models.Index(fields=['tag'], name='idx_tags_tag'),
        ]

    def __str__(self):
        return self.tag


class Question(models.Model):
    id_q = models.AutoField(primary_key=True, db_column='id_q')
    id_u = models.ForeignKey(User,on_delete=models.CASCADE,db_column='id_u')
    title_question = models.CharField(max_length=255, db_column='title_question')
    question = models.TextField(db_column='question')
    created_at_question = models.DateTimeField(default=timezone.now, db_column='created_at_question')
    has_answers = models.BooleanField(default=False, db_column='has_answers')
    correct_answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True, blank=True, db_column='correct_answer_id')

    tags = models.ManyToManyField(Tag, through='QuestionTag', related_name='questions')

    objects = models.Manager()
    class Meta:
        db_table = 'Questions'
        indexes = [models.Index(fields=['id_u'], name='idx_questions_user'),]

    def __str__(self):
        return self.title_question


class QuestionTag(models.Model):
    id_qt = models.AutoField(primary_key=True, db_column='id_qt')
    id_q = models.ForeignKey( Question, on_delete=models.CASCADE, db_column='id_q')
    id_t = models.ForeignKey(Tag, on_delete=models.RESTRICT, db_column='id_t')

    objects = models.Manager()
    class Meta:
        db_table = 'QuestionTags'
        unique_together = [['id_q', 'id_t']]
        indexes = [
            models.Index(fields=['id_q'], name='idx_questiontags_question'),
            models.Index(fields=['id_t'], name='idx_questiontags_tag'),
        ]

    def __str__(self):
        return f"Тег {self.id_t.tag} для вопроса {self.id_q.id_q}"


class Answer(models.Model):
    id_an = models.AutoField(primary_key=True, db_column='id_an')
    id_u = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, db_column='id_u')
    id_q = models.ForeignKey(Question, on_delete=models.CASCADE, db_column='id_q')
    answers = models.TextField(db_column='answers')
    created_at_answer = models.DateTimeField(default=timezone.now, db_column='created_at_answer')

    objects = models.Manager()
    class Meta:
        db_table = 'Answers'
        indexes = [
            models.Index(fields=['id_q'], name='idx_answers_question'),
            models.Index(fields=['id_u'], name='idx_answers_user'),
        ]

    def __str__(self):
        return f"Ответ на вопрос #{self.id_q.id_q}"


class QuestionVote(models.Model):
    id_vq = models.AutoField(primary_key=True, db_column='id_vq')
    id_u = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_u')
    id_q = models.ForeignKey(Question, on_delete=models.CASCADE, db_column='id_q')
    vote_value = models.SmallIntegerField(db_column='vote_value')

    objects = models.Manager()
    class Meta:
        db_table = 'QuestionVotes'
        unique_together = [['id_u', 'id_q']]

    def __str__(self):
        return f"Голос {self.vote_value} за вопрос #{self.id_q.id_q}"


class Vote(models.Model):
    id_v = models.AutoField(primary_key=True, db_column='id_v')
    id_u = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_u')
    id_an = models.ForeignKey(Answer, on_delete=models.CASCADE, db_column='id_an')
    vote_value = models.SmallIntegerField(db_column='vote_value')

    objects = models.Manager()
    class Meta:
        db_table = 'Votes'
        unique_together = [['id_u', 'id_an']]

    def __str__(self):
        return f"Голос {self.vote_value} за ответ #{self.id_an.id_an}"