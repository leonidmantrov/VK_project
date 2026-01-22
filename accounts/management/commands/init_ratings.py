from django.core.management.base import BaseCommand
from django.db.models import Sum, OuterRef, Subquery, Value, IntegerField
from django.db.models.functions import Coalesce
from django.db import transaction
import time
from accounts.models import User
from questions.models import Question, Answer


class Command(BaseCommand):
    help = 'Инициализирует рейтинг для всех пользователей'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Запуск оптимизированного пересчета...')
        start = time.time()

        question_votes = Question.objects.filter(user_id=OuterRef('pk')
        ).values('user_id').annotate(total=Sum('received_question_votes__vote_value')).values('total')[:1]

        answer_votes = Answer.objects.filter(user_id=OuterRef('pk')
        ).values('user_id').annotate(total=Sum('received_answer_votes__vote_value')).values('total')[:1]

        with transaction.atomic():
            updated = User.objects.update(
                rating=Coalesce(Subquery(question_votes, output_field=IntegerField()),Value(0))
                       + Coalesce(Subquery(answer_votes, output_field=IntegerField()),Value(0)))

        elapsed = time.time() - start

        self.stdout.write(self.style.SUCCESS(f'Обновлено {updated} пользователей за {elapsed:.1f}с'))