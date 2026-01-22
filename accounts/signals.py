from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from questions.models import QuestionVote, Vote


@receiver(post_save, sender=QuestionVote)
def on_new_question_vote(sender, instance, created, **kwargs):
    if created and instance.question and instance.question.user:
        instance.question.user.update_rating(delta=instance.vote_value)

@receiver(post_delete, sender=QuestionVote)
def on_delete_question_vote(sender, instance, **kwargs):
    if instance.question and instance.question.user:
        instance.question.user.update_rating(delta=-instance.vote_value)

@receiver(post_save, sender=Vote)
def on_new_answer_vote(sender, instance, created, **kwargs):
    if created and instance.answer and instance.answer.user:
        instance.answer.user.update_rating(delta=instance.vote_value)

@receiver(post_delete, sender=Vote)
def on_delete_answer_vote(sender, instance, **kwargs):
    if instance.answer and instance.answer.user:
        instance.answer.user.update_rating(delta=-instance.vote_value)