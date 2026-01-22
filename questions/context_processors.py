from django.db import models
from django.core.cache import cache
from questions.models import Tag
from accounts.models import User


def popular_tags_and_members(request):
    cache_key_tags = 'popular_tags'
    popular_tags = cache.get(cache_key_tags)

    if popular_tags is None:
        popular_tags = Tag.objects.annotate(num_questions=models.Count('tagged_questions')).order_by('-num_questions')[:10]
        cache.set(cache_key_tags, popular_tags, 300) #5 минут

    best_members = User.objects.all().order_by('-rating', '-date_joined')[:10]

    return {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }