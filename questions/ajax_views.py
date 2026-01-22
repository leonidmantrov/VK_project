from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from django.db.models import F
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

        question_text = Question.objects.get(id=question_id)

        # Проверяем, не пытается ли пользователь голосовать за свой вопрос
        if question_text.user == request.user:
            return JsonResponse({'error': 'Нельзя голосовать за свой вопрос'}, status=403)

        vote, created = QuestionVote.objects.update_or_create(
            user=request.user,
            question=question_text,
            defaults={'vote_value': vote_value}
        )

        question_text.refresh_from_db()

        return JsonResponse({
            'success': True,
            'rating': question_text.rating,
            'total_votes': question_text.total_votes,
            'user_vote': vote_value  # Всегда возвращаем значение кнопки
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

        answer = Answer.objects.get(id=answer_id)

        if answer.user == request.user:
            return JsonResponse({'error': 'Нельзя голосовать за свой ответ'}, status=403)

        vote, created = Vote.objects.update_or_create(
            user=request.user,
            answer=answer,
            defaults={'vote_value': vote_value}
        )

        answer.refresh_from_db()

        return JsonResponse({
            'success': True,
            'rating': answer.rating,
            'total_votes': answer.total_votes,
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

        question_text = Question.objects.get(id=question_id)

        # Проверяем, что пользователь - автор вопроса
        if question_text.user != request.user:
            return JsonResponse({'error': 'Только автор вопроса может отмечать правильный ответ'}, status=403)

        answer = Answer.objects.get(id=answer_id)

        # Проверяем, что ответ принадлежит этому вопросу
        if answer.question != question_text:
            return JsonResponse({'error': 'Ответ не принадлежит этому вопросу'}, status=400)

        # Если уже был правильный ответ - снимаем отметку
        if question_text.correct_answer == answer:
            question_text.correct_answer = None
        else:
            question_text.correct_answer = answer

        question_text.save()

        return JsonResponse({
            'success': True,
            'message': 'Правильный ответ отмечен',
            'is_correct': question_text.correct_answer_id == answer_id
        })

    except (Question.DoesNotExist, Answer.DoesNotExist):
        return JsonResponse({'error': 'Вопрос или ответ не найдены'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)