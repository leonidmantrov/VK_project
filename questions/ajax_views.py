from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from .models import Question, Answer, Vote, QuestionVote


@require_POST
@login_required
def vote_question(request):
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        vote_value = int(data.get('vote_value', 0))

        if vote_value not in [1, -1]:
            return JsonResponse({'error': 'Неверное значение голоса'}, status=400)

        question = Question.objects.get(id_q=question_id)

        # Создаем или обновляем голос
        vote, created = QuestionVote.objects.update_or_create(
            id_u=request.user,
            id_q=question,
            defaults={'vote_value': vote_value}
        )

        # Считаем новый рейтинг
        total_votes = QuestionVote.objects.filter(id_q=question).count()
        positive_votes = QuestionVote.objects.filter(id_q=question, vote_value=1).count()
        rating = positive_votes - (total_votes - positive_votes)

        return JsonResponse({
            'success': True,
            'rating': rating,
            'total_votes': total_votes,
            'user_vote': vote_value
        })

    except Question.DoesNotExist:
        return JsonResponse({'error': 'Вопрос не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
@login_required
def vote_answer(request):
    try:
        data = json.loads(request.body)
        answer_id = data.get('answer_id')
        vote_value = int(data.get('vote_value', 0))

        if vote_value not in [1, -1]:
            return JsonResponse({'error': 'Неверное значение голоса'}, status=400)

        answer = Answer.objects.get(id_an=answer_id)

        # Создаем или обновляем голос
        vote, created = Vote.objects.update_or_create(
            id_u=request.user,
            id_an=answer,
            defaults={'vote_value': vote_value}
        )

        # Считаем рейтинг
        total_votes = Vote.objects.filter(id_an=answer).count()
        positive_votes = Vote.objects.filter(id_an=answer, vote_value=1).count()
        rating = positive_votes - (total_votes - positive_votes)

        return JsonResponse({
            'success': True,
            'rating': rating,
            'total_votes': total_votes,
            'user_vote': vote_value
        })

    except Answer.DoesNotExist:
        return JsonResponse({'error': 'Ответ не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
@login_required
def mark_correct_answer(request):
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        answer_id = data.get('answer_id')

        question = Question.objects.get(id_q=question_id)

        # Проверяем, что пользователь - автор вопроса
        if question.id_u != request.user:
            return JsonResponse({'error': 'Только автор вопроса может отмечать правильный ответ'}, status=403)

        answer = Answer.objects.get(id_an=answer_id)

        # Проверяем, что ответ принадлежит этому вопросу
        if answer.id_q != question:
            return JsonResponse({'error': 'Ответ не принадлежит этому вопросу'}, status=400)

        # Устанавливаем правильный ответ
        question.correct_answer = answer
        question.save()

        return JsonResponse({
            'success': True,
            'message': 'Правильный ответ отмечен'
        })

    except (Question.DoesNotExist, Answer.DoesNotExist):
        return JsonResponse({'error': 'Вопрос или ответ не найдены'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)