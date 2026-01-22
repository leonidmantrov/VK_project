from django.db import models
from .manager import QuestionManager, AnswerManager

class Tag(models.Model):
    tag_text = models.CharField(max_length=50, unique=True)

    objects = models.Manager()
    class Meta:
        db_table = 'Tags'
        indexes = [models.Index(fields=['tag_text'], name='idx_tags_tag')]

    def __str__(self):
        return self.tag_text


class Question(models.Model):
    title_question = models.CharField(max_length=255)
    question_text = models.TextField(max_length=1000)
    created_at_question = models.DateTimeField(auto_now_add=True)
    has_answers = models.BooleanField(default=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='authored_questions')
    correct_answer = models.ForeignKey('questions.Answer', on_delete=models.SET_NULL, related_name='marked_correct_in', null=True, blank=True)

    rating = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)

    tags = models.ManyToManyField('questions.Tag', through='QuestionTag', related_name='tagged_questions')

    objects = QuestionManager()

    class Meta:
        db_table = 'Questions'

    def __str__(self):
        return self.title_question


class QuestionTag(models.Model):
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='tag_links')
    tag = models.ForeignKey('questions.Tag', on_delete=models.RESTRICT, related_name='question_links')

    objects = models.Manager()
    class Meta:
        db_table = 'QuestionTags'
        unique_together = [['question', 'tag']]

    def __str__(self):
        return f"Тег {self.tag.tag_text} для вопроса {self.question.id}"


class Answer(models.Model):
    answer_text = models.TextField(max_length=1000)
    created_at_answer = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='authored_answers', null=True)
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='received_answers')

    rating = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)

    objects = AnswerManager()
    class Meta:
        db_table = 'Answers'

    def __str__(self):
        return f"Ответ на вопрос #{self.question.id}"


class QuestionVote(models.Model):
    vote_value = models.SmallIntegerField()
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='given_question_votes')
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='received_question_votes')

    objects = models.Manager()
    class Meta:
        db_table = 'QuestionVotes'
        unique_together = [['user', 'question']]

    def __str__(self):
        return f"Голос {self.vote_value} за вопрос #{self.question.id}"


class Vote(models.Model):
    vote_value = models.SmallIntegerField()
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='given_answer_votes')
    answer = models.ForeignKey('questions.Answer', on_delete=models.CASCADE, related_name='received_answer_votes')

    objects = models.Manager()
    class Meta:
        db_table = 'Votes'
        unique_together = [['user', 'answer']]

    def __str__(self):
        return f"Голос {self.vote_value} за ответ #{self.answer.id}"