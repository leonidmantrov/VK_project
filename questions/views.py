from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from questions.models import Question, Answer, Tag, QuestionVote, Vote
from accounts.models import User
from django.core.paginator import Paginator
from .forms import QuestionForm


# def questions_page(request):
#     questions_list = Question.objects.for_questions_page()
#
#     paginator = Paginator(questions_list, per_page=5)
#     page = request.GET.get('page', 1)
#
#     return render(request, 'so_project/index.html', {
#         "questions_page": paginator.page(page),
#         "sorting_type": "new_questions",
#     })

def questions_page(request):
    questions_list = Question.objects.for_questions_page()

    # Добавляем user_vote к УЖЕ отсортированным вопросам
    questions_list = Question.objects.with_user_votes(request.user, questions_list)

    paginator = Paginator(questions_list, per_page=5)
    page = request.GET.get('page', 1)

    return render(request, 'so_project/index.html', {
        "questions_page": paginator.page(page),
        "sorting_type": "new_questions",
    })

# def answers_page_for_question(request, id):
#     question_text = Question.objects.with_answers_for_question(id)
#
#     if not question_text:
#         return redirect('questions:questions_page')
#
#     answer_text = Answer.objects.with_user_votes(id, request.user)
#
#     for answer in answer_text:
#         answer.is_correct = (question_text.correct_answer_id == answer.id)
#
#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             return redirect('accounts:login_page')
#
#         answer_text_content = request.POST.get('answer_text', '').strip()
#
#         if answer_text_content:
#             Answer.objects.create(
#                 answer_text=answer_text_content,
#                 question=question_text,
#                 user=request.user
#             )
#             return redirect('questions:answers_page_for_question', id=id)
#
#     can_mark_correct = request.user.is_authenticated and question_text.user == request.user
#
#     return render(request, 'so_project/pageForOneQuestion.html', {
#         "question_text": question_text,
#         "answer_text": answer_text,
#         "can_mark_correct": can_mark_correct,
#         "user": request.user
#     })

# questions/views.py - функция answers_page_for_question
def answers_page_for_question(request, id):
    question_text = Question.objects.with_answers_for_question(id)

    if not question_text:
        return redirect('questions:questions_page')

    # Используем менеджер для ответов с user_vote
    answer_text = Answer.objects.with_user_votes(id, request.user)

    # Отмечаем правильные ответы
    for answer in answer_text:
        answer.is_correct = (question_text.correct_answer_id == answer.id)

    # Добавляем user_vote для вопроса
    if request.user.is_authenticated:
        from .models import QuestionVote
        try:
            question_vote = QuestionVote.objects.get(
                user=request.user,
                question=question_text
            )
            question_text.user_vote = question_vote.vote_value
        except QuestionVote.DoesNotExist:
            question_text.user_vote = 0
    else:
        question_text.user_vote = 0

    # Остальной код без изменений...
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login_page')

        answer_text_content = request.POST.get('answer_text', '').strip()

        if answer_text_content:
            Answer.objects.create(
                answer_text=answer_text_content,
                question=question_text,
                user=request.user
            )
            return redirect('questions:answers_page_for_question', id=id)

    can_mark_correct = request.user.is_authenticated and question_text.user == request.user

    return render(request, 'so_project/pageForOneQuestion.html', {
        "question_text": question_text,
        "answer_text": answer_text,
        "can_mark_correct": can_mark_correct,
        "user": request.user
    })

@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(data=request.POST, user=request.user)
        if form.is_valid():
            question = form.save()
            return redirect('questions:answers_page_for_question', id=question.pk)
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = QuestionForm(user=request.user)

    return render(request, 'so_project/add_question.html', {'form': form})

# def questions_by_tag(request):
#     tag_for_question = request.GET.get('tag_name', '').strip()
#
#     if tag_for_question.startswith('[') and tag_for_question.endswith(']'):
#         actual_tag = tag_for_question[1:-1]
#     else:
#         actual_tag = tag_for_question
#
#     if not actual_tag:
#         return redirect('questions:questions_page')
#
#     questions_list = Question.objects.by_tag(actual_tag)
#
#     paginator = Paginator(questions_list, per_page=5)
#     page = request.GET.get('page', 1)
#     questions_page = paginator.page(page)
#
#     return render(request, 'so_project/questions_by_tag.html', {
#         "questions_page": questions_page,
#         "current_tag": actual_tag,
#     })

def questions_by_tag(request):
    tag_for_question = request.GET.get('tag_name', '').strip()

    if tag_for_question.startswith('[') and tag_for_question.endswith(']'):
        actual_tag = tag_for_question[1:-1]
    else:
        actual_tag = tag_for_question

    if not actual_tag:
        return redirect('questions:questions_page')

    questions_list = Question.objects.by_tag(actual_tag)

    # Добавляем user_vote к УЖЕ отсортированным вопросам
    questions_list = Question.objects.with_user_votes(request.user, questions_list)

    paginator = Paginator(questions_list, per_page=5)
    page = request.GET.get('page', 1)
    questions_page = paginator.page(page)

    return render(request, 'so_project/questions_by_tag.html', {
        "questions_page": questions_page,
        "current_tag": actual_tag,
    })

def profile_member(request, id):
    user = get_object_or_404(User, pk=id)

    user_questions = Question.objects.with_all_relations().filter(user=user).order_by('-created_at_question')
    user_answers = Answer.objects.with_all_relations().filter(user=user).order_by('-created_at_answer')

    return render(request, 'so_project/profile_members.html', {
        "profile_user": user,
        "user_questions": user_questions,
        "user_answers": user_answers,
    })


# def hot_questions_page(request):
#     questions_list = Question.objects.for_hot_questions()
#
#     paginator = Paginator(questions_list, per_page=5)
#     page = request.GET.get('page', 1)
#
#     return render(request, 'so_project/index.html', {
#         "questions_page": paginator.page(page),
#         "sorting_type": "hot_questions",
#     })

def hot_questions_page(request):
    questions_list = Question.objects.for_hot_questions()

    # Добавляем user_vote к УЖЕ отсортированным вопросам
    questions_list = Question.objects.with_user_votes(request.user, questions_list)

    paginator = Paginator(questions_list, per_page=5)
    page = request.GET.get('page', 1)

    return render(request, 'so_project/index.html', {
        "questions_page": paginator.page(page),
        "sorting_type": "hot_questions",
    })
