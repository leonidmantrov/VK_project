from django.db.models import Count, Case, When, IntegerField, Sum
from django.db.models.functions import Coalesce
from .models import Tag, User


def popular_tags_and_members(request):

    # 10 самых часто используемых тегов
    popular_tags = Tag.objects.annotate(
        num_questions=Count('questions')
    ).order_by('-num_questions')[:10]

    # 10 пользователей с наибольшим рейтингом (по лайкам вопросов + ответов)
    best_members = User.objects.annotate(
        question_rating=Coalesce(
            Sum(
                Case(
                    When(question__questionvote__vote_value=1, then=1),
                    When(question__questionvote__vote_value=-1, then=-1),
                    default=0,
                    output_field=IntegerField()
                )
            ), 0
        ),
        answer_rating=Coalesce(
            Sum(
                Case(
                    When(answer__vote__vote_value=1, then=1),
                    When(answer__vote__vote_value=-1, then=-1),
                    default=0,
                    output_field=IntegerField()
                )
            ), 0
        ),
        num_questions=Count('question', distinct=True),
        num_answers=Count('answer', distinct=True)
    ).annotate(
        total_rating=Case(
            When(question_rating__isnull=True, answer_rating__isnull=True, then=0),
            default=Coalesce('question_rating', 0) + Coalesce('answer_rating', 0),
            output_field=IntegerField()
        )
    ).order_by('-total_rating', '-num_questions', '-num_answers')[:10]

    return {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }