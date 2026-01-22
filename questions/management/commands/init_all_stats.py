from django.core.management.base import BaseCommand
from django.db.models import Sum, Count, OuterRef, Subquery, Value, Exists, IntegerField
from django.db.models.functions import Coalesce
from questions.models import Question, Answer, QuestionVote, Vote


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Вопросы...')
        Question.objects.update(
            rating=Coalesce(Subquery(
                QuestionVote.objects.filter(question_id=OuterRef('pk'))
                .values('question_id').annotate(s=Sum('vote_value')).values('s')[:1],
                output_field=IntegerField()
            ), 0),
            total_votes=Coalesce(Subquery(
                QuestionVote.objects.filter(question_id=OuterRef('pk'))
                .values('question_id').annotate(c=Count('id')).values('c')[:1],
                output_field=IntegerField()
            ), 0),
            answers_count=Coalesce(Subquery(
                Answer.objects.filter(question_id=OuterRef('pk'))
                .values('question_id').annotate(c=Count('id')).values('c')[:1],
                output_field=IntegerField()
            ), 0),
            has_answers=Exists(Answer.objects.filter(question_id=OuterRef('pk')))
        )

        print('Ответы...')
        Answer.objects.update(
            rating=Coalesce(Subquery(
                Vote.objects.filter(answer_id=OuterRef('pk'))
                .values('answer_id').annotate(s=Sum('vote_value')).values('s')[:1],
                output_field=IntegerField()
            ), 0),
            total_votes=Coalesce(Subquery(
                Vote.objects.filter(answer_id=OuterRef('pk'))
                .values('answer_id').annotate(c=Count('id')).values('c')[:1],
                output_field=IntegerField()
            ), 0)
        )

        print('Готово!')