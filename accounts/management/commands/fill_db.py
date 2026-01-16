import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from faker import Faker
from accounts.models import User
from questions.models import Question, Answer, Tag, QuestionVote, Vote, QuestionTag


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio',type=int, help='Коэффициент заполнения сущностей')
        parser.add_argument('--batch-size',type=int,default=500,help='Размер батча для bulk_create')

    def handle(self, *args, **options):
        ratio = options['ratio']
        batch_size = options['batch_size']
        fake = Faker(['ru_RU'])

        self.stdout.write(self.style.SUCCESS(
            f'Начинаем заполнение БД с коэффициентом {ratio}...'
        ))
        self.reset_database()

        with transaction.atomic():
            self.stdout.write(f'1. Создаем {ratio} пользователей...')
            users = self.create_users(ratio, fake, batch_size)
            self.stdout.write(self.style.SUCCESS(f'   ✓ Создано {len(users)} пользователей'))

            self.stdout.write(f'2. Создаем {ratio} тегов...')
            tags = self.create_tags(ratio, fake, batch_size)
            self.stdout.write(self.style.SUCCESS(f'   ✓ Создано {len(tags)} тегов'))

            num_questions = ratio * 10
            self.stdout.write(f'3. Создаем {num_questions} вопросов...')
            questions = self.create_questions(num_questions, users, fake, batch_size)
            self.stdout.write(self.style.SUCCESS(f'   ✓ Создано {len(questions)} вопросов'))

            self.stdout.write('4. Создаем связи вопрос-тег...')
            links_count = self.create_question_tags(questions, tags, batch_size)
            self.stdout.write(self.style.SUCCESS(f'   ✓ Создано {links_count} связей'))

            num_answers = ratio * 100
            self.stdout.write(f'5. Создаем {num_answers} ответов...')
            answers = self.create_answers(num_answers, users, questions, fake, batch_size)
            self.stdout.write(self.style.SUCCESS(f'   ✓ Создано {len(answers)} ответов'))

            num_votes = ratio * 200
            self.stdout.write(f'6. Создаем {num_votes} голосов...')
            votes_count = self.create_votes(num_votes, users, questions, answers, batch_size)
            self.stdout.write(self.style.SUCCESS(f'   ✓ Создано {votes_count} голосов'))

        self.print_statistics()

    def reset_database(self):
        Vote.objects.all().delete()
        QuestionVote.objects.all().delete()
        Answer.objects.all().delete()
        QuestionTag.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()

    def create_users(self, num_users, fake, batch_size):
        users = []
        existing_logins = set(User.objects.values_list('login', flat=True))

        for i in range(num_users):
            while True:
                login = f'user_{i}_{fake.user_name()}'[:30]
                if login not in existing_logins:
                    existing_logins.add(login)
                    break

            users.append(User(
                login=login,
                email=f'user_{i}@{fake.domain_name()}',
                nickname=fake.first_name()[:30],
                password='password123',
                is_active=True,
                date_joined=fake.date_time_between(
                    start_date='-2y',
                    end_date='now',
                    tzinfo=timezone.get_current_timezone()
                )
            ))

        User.objects.bulk_create(users, batch_size=batch_size)
        return list(User.objects.filter(login__in=[u.login for u in users]))

    def create_tags(self, num_tags, fake, batch_size):
        tags = []
        existing_tags = set(Tag.objects.values_list('tag', flat=True))

        for i in range(num_tags):
            while True:
                tag_name = fake.word()
                if tag_name not in existing_tags:
                    existing_tags.add(tag_name)
                    break

            tags.append(Tag(tag=tag_name[:50]))

        Tag.objects.bulk_create(tags, batch_size=batch_size)
        return list(Tag.objects.filter(tag__in=[t.tag for t in tags]))

    def create_questions(self, num_questions, users, fake, batch_size):
        questions = []

        for i in range(num_questions):
            user = random.choice(users)
            questions.append(Question(
                id_u=user,
                title_question=fake.sentence()[:250],
                question=fake.text(max_nb_chars=1000),
                created_at_question=fake.date_time_between(
                    start_date=user.date_joined,
                    end_date='now',
                    tzinfo=timezone.get_current_timezone()
                ),
                has_answers=False
            ))

        Question.objects.bulk_create(questions, batch_size=batch_size)
        return list(Question.objects.order_by('-created_at_question')[:num_questions])

    def create_question_tags(self, questions, tags, batch_size):
        if not questions or not tags:
            return 0

        question_tags = []

        for question in questions:
            num_tags = random.randint(1, min(3, len(tags)))
            selected_tags = random.sample(tags, num_tags)

            for tag in selected_tags:
                question_tags.append(QuestionTag(
                    id_q=question,
                    id_t=tag
                ))

        if question_tags:
            QuestionTag.objects.bulk_create(question_tags, batch_size=batch_size)

        return len(question_tags)

    def create_answers(self, num_answers, users, questions, fake, batch_size):
        if not questions:
            self.stdout.write(self.style.WARNING('   Нет вопросов для ответов!'))
            return []

        answers = []

        for i in range(num_answers):
            question = random.choice(questions)
            user = random.choice(users)

            answers.append(Answer(
                id_u=user,
                id_q=question,
                answers=fake.text(max_nb_chars=500),
                created_at_answer=fake.date_time_between(
                    start_date=question.created_at_question,
                    end_date='now',
                    tzinfo=timezone.get_current_timezone()
                )
            ))

        Answer.objects.bulk_create(answers, batch_size=batch_size)

        question_ids_with_answers = Answer.objects.values_list('id_q_id', flat=True).distinct()
        Question.objects.filter(id_q__in=question_ids_with_answers).update(has_answers=True)

        return list(Answer.objects.order_by('-created_at_answer')[:num_answers])

    def create_votes(self, num_votes, users, questions, answers, batch_size):
        total_votes = 0

        # Голоса за вопросы
        if questions:
            question_votes = []
            existing_votes = set()

            # Получаем существующие голоса
            existing_q_votes = QuestionVote.objects.filter(
                id_u__in=[u.id for u in users],
                id_q__in=[q.id_q for q in questions]
            ).values_list('id_u_id', 'id_q_id')
            existing_votes.update(existing_q_votes)

            # Новые голоса
            max_possible = len(users) * len(questions)
            votes_to_create = min(num_votes // 2, max_possible - len(existing_q_votes))

            created = 0
            attempts = 0
            max_attempts = votes_to_create * 10

            while created < votes_to_create and attempts < max_attempts:
                user = random.choice(users)
                question = random.choice(questions)

                key = (user.id, question.id_q)
                if key not in existing_votes:
                    question_votes.append(QuestionVote(
                        id_u=user,
                        id_q=question,
                        vote_value=random.choice([1, -1])
                    ))
                    existing_votes.add(key)
                    created += 1
                attempts += 1

            if question_votes:
                for i in range(0, len(question_votes), batch_size):
                    batch = question_votes[i:i + batch_size]
                    QuestionVote.objects.bulk_create(batch, ignore_conflicts=True)

                total_votes += len(question_votes)
                self.stdout.write(self.style.SUCCESS(f'   → {len(question_votes)} голосов за вопросы'))

        # Голоса за ответы
        if answers:
            answer_votes = []
            existing_votes = set()

            # Существующие голоса за ответы
            existing_a_votes = Vote.objects.filter(
                id_u__in=[u.id for u in users],
                id_an__in=[a.id_an for a in answers]
            ).values_list('id_u_id', 'id_an_id')
            existing_votes.update(existing_a_votes)

            # Новые голоса
            max_possible = len(users) * len(answers)
            votes_to_create = min(num_votes // 2, max_possible - len(existing_a_votes))

            created = 0
            attempts = 0
            max_attempts = votes_to_create * 10

            while created < votes_to_create and attempts < max_attempts:
                user = random.choice(users)
                answer = random.choice(answers)

                key = (user.id, answer.id_an)
                if key not in existing_votes:
                    answer_votes.append(Vote(
                        id_u=user,
                        id_an=answer,
                        vote_value=random.choice([1, -1])
                    ))
                    existing_votes.add(key)
                    created += 1
                attempts += 1

            if answer_votes:
                for i in range(0, len(answer_votes), batch_size):
                    batch = answer_votes[i:i + batch_size]
                    Vote.objects.bulk_create(batch, ignore_conflicts=True)

                total_votes += len(answer_votes)
                self.stdout.write(self.style.SUCCESS(f'   → {len(answer_votes)} голосов за ответы'))

        return total_votes

    def print_statistics(self):
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))
        self.stdout.write(self.style.SUCCESS('СТАТИСТИКА:'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'Пользователи: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Вопросы: {Question.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Ответы: {Answer.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Теги: {Tag.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Голоса за вопросы: {QuestionVote.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Голоса за ответы: {Vote.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))