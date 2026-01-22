from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import QuestionVote, Vote, Answer, Question


@receiver(post_save, sender=QuestionVote)
def update_question_stats_on_vote_create(sender, instance, created, **kwargs):
    if created and instance.question_id:
        Question.objects.filter(id=instance.question_id).update(rating=F('rating') + instance.vote_value,total_votes=F('total_votes') + 1)

@receiver(post_delete, sender=QuestionVote)
def revert_question_stats_on_vote_delete(sender, instance, **kwargs):
    if instance.question_id:
        Question.objects.filter(id=instance.question_id).update(rating=F('rating') - instance.vote_value,total_votes=F('total_votes') - 1)

@receiver(post_save, sender=Vote)
def update_answer_stats_on_vote_create(sender, instance, created, **kwargs):
    if created and instance.answer_id:
        Answer.objects.filter(id=instance.answer_id).update(rating=F('rating') + instance.vote_value,total_votes=F('total_votes') + 1)

@receiver(post_delete, sender=Vote)
def revert_answer_stats_on_vote_delete(sender, instance, **kwargs):
    if instance.answer_id:
        Answer.objects.filter(id=instance.answer_id).update(rating=F('rating') - instance.vote_value,total_votes=F('total_votes') - 1)

@receiver(post_save, sender=Answer)
def update_question_on_answer_create(sender, instance, created, **kwargs):
    if created and instance.question_id:
        Question.objects.filter(id=instance.question_id).update(answers_count=F('answers_count') + 1,has_answers=True)

@receiver(post_delete, sender=Answer)
def update_question_on_answer_delete(sender, instance, **kwargs):
    if instance.question_id:
        Question.objects.filter(id=instance.question_id).update(answers_count=F('answers_count') - 1)
        remaining_answers = Answer.objects.filter(question_id=instance.question_id).exists()

        if not remaining_answers:
            Question.objects.filter(id=instance.question_id).update(has_answers=False)