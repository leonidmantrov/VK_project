from django.db.models import Manager, Prefetch


class QuestionManager(Manager):
    def with_all_relations(self):
        from questions.models import Tag
        return self.get_queryset().select_related('user').prefetch_related(
            Prefetch('tags', queryset=Tag.objects.only('tag_text'))
        ).only(
            'id', 'title_question', 'question_text', 'created_at_question',
            'rating', 'total_votes', 'answers_count', 'has_answers',
            'user_id', 'correct_answer_id'
        )

    def with_user_votes(self, user, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        questions = list(queryset)

        if user.is_authenticated:
            from .models import QuestionVote
            question_ids = [q.id for q in questions]
            user_votes = QuestionVote.objects.filter(
                user=user,
                question_id__in=question_ids
            ).values('question_id', 'vote_value')

            user_votes_dict = {v['question_id']: v['vote_value'] for v in user_votes}

            for question in questions:
                question.user_vote = user_votes_dict.get(question.id, 0)
        else:
            for question in questions:
                question.user_vote = 0

        return questions

    def for_questions_page(self):
        return self.with_all_relations().order_by('-created_at_question')

    def for_question_page(self, question_id):
        return self.with_all_relations().filter(id=question_id).first()

    def for_hot_questions(self):
        return self.with_all_relations().order_by('-answers_count', '-rating', '-created_at_question')

    def by_tag(self, tag_name):
        return self.with_all_relations().filter(
            tags__tag_text=tag_name
        ).order_by('-created_at_question')

    def with_answers_for_question(self, question_id):
        return self.with_all_relations().filter(id=question_id).first()


class AnswerManager(Manager):
    def with_all_relations(self):
        return self.get_queryset().select_related(
            'user', 'question'
        ).only(
            'id', 'answer_text', 'created_at_answer',
            'rating', 'total_votes',
            'user_id', 'question_id'
        )

    def for_question_page(self, question_id):
        return self.with_all_relations().filter(
            question_id=question_id
        ).order_by('-rating', '-created_at_answer')

    def with_user_votes(self, question_id, user):
        answers = self.for_question_page(question_id)

        if user.is_authenticated:
            from .models import Vote
            user_votes = Vote.objects.filter(
                user=user,
                answer_id__in=[a.id for a in answers]
            ).values('answer', 'vote_value')

            user_votes_dict = {v['answer']: v['vote_value'] for v in user_votes}

            for answer in answers:
                answer.user_vote = user_votes_dict.get(answer.id, 0)
        else:
            for answer in answers:
                answer.user_vote = 0

        return answers
