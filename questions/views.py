from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, Tag, User, QuestionVote, Vote
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Case, When, IntegerField, Q
from django.db.models.functions import Coalesce
from django.conf import settings

def questions_page(request):
    questions_list = Question.objects.select_related('id_u').prefetch_related('tags').annotate(
        rating=Coalesce(
            Sum(
                Case(
                    When(questionvote__vote_value=1, then=1),
                    When(questionvote__vote_value=-1, then=-1),
                    default=0,
                    output_field=IntegerField()
                )
            ), 0
        ),
        total_votes=Count('questionvote'),
        answers_count=Count('answer')
    ).order_by('-created_at_question')

    if request.user.is_authenticated:
        user_votes = QuestionVote.objects.filter(
            id_u=request.user,
            id_q__in=[q.id_q for q in questions_list]
        ).values('id_q', 'vote_value')
        user_votes_dict = {v['id_q']: v['vote_value'] for v in user_votes}

        for question in questions_list:
            question.user_vote = user_votes_dict.get(question.id_q, 0)
    else:
        for question in questions_list:
            question.user_vote = 0

    paginator = Paginator(questions_list, per_page=2)
    page = request.GET.get('page', 1)
    questions_page = paginator.page(page)

    return render(request, 'so_project/index.html', {
        "questions_page": questions_page,
        "user": request.user
    })

def answers_page_for_question(request, id):
    question = get_object_or_404(Question, id_q=id)

    answers = Answer.objects.filter(id_q=question).select_related('id_u').annotate(
        rating=Coalesce(
            Sum(
                Case(
                    When(vote__vote_value=1, then=1),
                    When(vote__vote_value=-1, then=-1),
                    default=0,
                    output_field=IntegerField()
                )
            ), 0
        ),
        total_votes=Count('vote')
    ).order_by('-created_at_answer')

    if request.user.is_authenticated:
        user_votes = Vote.objects.filter(
            id_u=request.user,
            id_an__in=[a.id_an for a in answers]
        ).values('id_an', 'vote_value')

        user_votes_dict = {v['id_an']: v['vote_value'] for v in user_votes}

        for answer in answers:
            answer.user_vote = user_votes_dict.get(answer.id_an, 0)
            answer.is_correct = (question.correct_answer_id == answer.id_an)
    else:
        for answer in answers:
            answer.user_vote = 0
            answer.is_correct = (question.correct_answer_id == answer.id_an)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login_page')

        answer_text = request.POST.get('answer_text', '').strip()

        if answer_text:
            Answer.objects.create(
                answers=answer_text,
                id_q=question,
                id_u=request.user
            )
            return redirect('questions:answers_page_for_question', id=id)

    can_mark_correct = request.user.is_authenticated and question.id_u == request.user

    return render(request, 'so_project/pageForOneQuestion.html', {
        "question": question,
        "answers": answers,
        "can_mark_correct": can_mark_correct,
        "user": request.user
    })

@login_required
def add_question(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        text = request.POST.get('text', '').strip()
        tags_input = request.POST.get('tags', '').strip()

        if title and text:
            question = Question.objects.create(
                title_question=title,
                question=text,
                id_u=request.user
            )
            if tags_input:
                for tag_name in tags_input.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(tag=tag_name)
                        question.tags.add(tag)

            return redirect('questions:answers_page_for_question', id=question.pk)

    return render(request, 'so_project/add_question.html')


def questions_by_tag(request):
    tag_for_question  = request.GET.get('tag_name', '')

    if tag_for_question .startswith('[') and tag_for_question .endswith(']'):
        actual_tag = tag_for_question [1:-1]
    else:
        return redirect('questions:questions_page')

    if actual_tag:
        try:
            tag = Tag.objects.get(tag=actual_tag)
            questions_list = Question.objects.filter(tags=tag).order_by('-created_at_question')
        except Tag.DoesNotExist:
            questions_list = Question.objects.none()
    else:
        return redirect('questions:questions_page')

    paginator = Paginator(questions_list, per_page=2)
    page = request.GET.get('page', 1)
    questions_page = paginator.page(page)

    return render(request, 'so_project/questions_by_tag.html', {
        "questions_page": questions_page,
        "current_tag": actual_tag,
    })


def profile_member(request, id):
    user = get_object_or_404(User, pk=id)

    user_questions = Question.objects.filter(id_u=user).order_by('-created_at_question')
    user_answers = Answer.objects.filter(id_u=user).order_by('-created_at_answer')

    print(f"DEBUG is currently set to: {settings.DEBUG}")

    return render(request, 'so_project/profile_members.html', {
        "profile_user": user,
        "user_questions": user_questions,
        "user_answers": user_answers,
    })