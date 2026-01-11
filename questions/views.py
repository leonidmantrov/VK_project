from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from project.mock_data import QUESTIONS, ANSWERS, PROFILE_MEMBERS


def questions_page(request, *args, **kwargs):
    paginator = Paginator(QUESTIONS, per_page=2)
    page = request.GET.get('page', 1)
    questions_page = paginator.page(page)
    return render(request, 'so_project/index.html', context={"questions_page": questions_page})


def answers_page_for_question(request, id):
    current_question = next((q for q in QUESTIONS if q["id"] == id), None)

    if current_question is None:
        from django.http import Http404
        raise Http404("Question not found")

    return render(request, 'so_project/pageForOneQuestion.html', context={
        "question": current_question,
        "answers": ANSWERS
    })

def questions_by_tag(request):
    tag_for_question = request.GET.get('tag_name', '')
    actual_tag = None

    if tag_for_question.startswith('[') and tag_for_question.endswith(']'):
        actual_tag = tag_for_question[1:-1]

    if actual_tag:
        good_questions = [q for q in QUESTIONS if actual_tag.lower() in [t.lower() for t in q['tags']]]

        paginator = Paginator(good_questions, per_page=2)
        page = request.GET.get('page', 1)
        questions_page  = paginator.page(page)

        return render(request, 'so_project/questions_by_tag.html', context={
            "questions_page": questions_page,
            "current_tag": actual_tag,
        })
    else:
        return redirect('questions_page')

def add_question(request):
    return render(request, 'so_project/add_question.html')

def profile_member(request, id):
    profile = next((q for q in PROFILE_MEMBERS if q["id"] == id), None)

    if profile is None:
        from django.http import Http404
        raise Http404("Profile not found")

    if not profile["Questions"]:
        profile["Questions"] = ["The user has not asked any questions yet"]
    if not profile["Answers"]:
        profile["Answers"] = ["The user has not yet answered anyone's questions"]

    return render(request, 'so_project/profile_members.html', context={
        "info_profile": profile,
    })