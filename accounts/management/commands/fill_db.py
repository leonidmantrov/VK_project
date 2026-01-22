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
            answer_text = self.create_answers(num_answers, users, questions, fake, batch_size)
            self.stdout.write(self.style.SUCCESS(f'   ✓ Создано {len(answer_text)} ответов'))

            num_votes = ratio * 200
            self.stdout.write(f'6. Создаем {num_votes} голосов...')
            votes_count = self.create_votes(num_votes, users, questions, answer_text, batch_size)
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
        self.stdout.write(f'   Генерация {num_tags} уникальных тегов...')

        # Генерируем с запасом
        needed = num_tags
        created_count = 0
        all_tags = []

        while created_count < num_tags:
            # Генерируем порцию с запасом 20%
            batch_needed = min((num_tags - created_count) * 12 // 10, 10000)
            candidates = set()

            while len(candidates) < batch_needed:
                candidates.add(fake.word().lower()[:50])

            # Проверяем существующие
            existing = set(Tag.objects.filter(
                tag_text__in=candidates
            ).values_list('tag_text', flat=True))

            # Создаем новые
            new_names = candidates - existing
            if not new_names:
                # Если все слова заняты, добавляем суффикс
                new_names = {f"{name}_{random.randint(1000, 9999)}" for name in candidates}

            tags = [Tag(tag_text=name) for name in new_names]
            Tag.objects.bulk_create(tags, batch_size=batch_size, ignore_conflicts=True)
            created_count += len(tags)
            all_tags.extend(tags)

            # Для очень больших объемов - промежуточный вывод
            if created_count % 10000 == 0:
                self.stdout.write(f'   Создано {created_count}/{num_tags} тегов...')

        # Возвращаем ВСЕ теги из базы для связей
        return list(Tag.objects.all())

    def create_questions(self, num_questions, users, fake, batch_size):
        questions = []

        for i in range(num_questions):
            user = random.choice(users)
            questions.append(Question(
                user=user,
                title_question=fake.sentence()[:250],
                question_text=fake.text(max_nb_chars=1000),
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

        # Подготовка данных
        tag_ids = [t.id for t in tags]
        question_ids = [q.id for q in questions]

        # Загружаем существующие связи одним запросом
        existing_pairs = set(
            QuestionTag.objects.filter(
                question_id__in=question_ids,
                tag_id__in=tag_ids
            ).values_list('question_id', 'tag_id')
        )

        question_tags = []
        created_count = 0

        for question in questions:
            # Выбираем уникальные теги для вопроса
            selected_ids = random.sample(tag_ids, random.randint(1, min(3, len(tag_ids))))

            for tid in selected_ids:
                pair = (question.id, tid)

                # Проверяем, не существует ли уже такая связь
                if pair not in existing_pairs:
                    question_tags.append(QuestionTag(
                        question_id=question.id,
                        tag_id=tid
                    ))
                    existing_pairs.add(pair)
                    created_count += 1

                    # Батч-вставка
                    if len(question_tags) >= batch_size:
                        QuestionTag.objects.bulk_create(question_tags, ignore_conflicts=True)
                        question_tags = []

        # Остатки
        if question_tags:
            QuestionTag.objects.bulk_create(question_tags, ignore_conflicts=True)

        return created_count

    def create_answers(self, num_answers, users, questions, fake, batch_size):
        if not questions:
            self.stdout.write(self.style.WARNING('   Нет вопросов для ответов!'))
            return []

        # Подготовка ID для генерации (но возвращать будем объекты)
        u_ids = [u.id for u in users]
        q_data = {q.id: q.created_at_question for q in questions}
        q_ids = list(q_data.keys())

        temp_answers = []
        self.stdout.write(f'   Создание {num_answers} ответов...')

        for i in range(num_answers):
            qid = random.choice(q_ids)

            temp_answers.append(Answer(
                user_id=random.choice(u_ids),
                question_id=qid,
                answer_text=fake.text(max_nb_chars=500),
                created_at_answer=fake.date_time_between(
                    start_date=q_data[qid],
                    end_date='now',
                    tzinfo=timezone.get_current_timezone()
                )
            ))

            # Сбрасываем пачками, чтобы Python не "съел" всю оперативку
            if len(temp_answers) >= batch_size:
                Answer.objects.bulk_create(temp_answers)
                temp_answers = []

        if temp_answers:
            Answer.objects.bulk_create(temp_answers)

        # 1. Обновляем статус вопросов в MySQL
        self.stdout.write('   Обновление статусов вопросов...')
        answered_q_ids = Answer.objects.values_list('question_id', flat=True).distinct()
        Question.objects.filter(id__in=answered_q_ids).update(has_answers=True)

        # 2. Возвращаем объекты.
        # ВАЖНО: Мы делаем срез [:num_answers], чтобы вернуть только то, что создали сейчас.
        # Мы перечитываем их из базы, чтобы у них появились ID, необходимые для голосов.
        self.stdout.write('   Загрузка объектов для следующего шага...')
        return list(Answer.objects.order_by('-id')[:num_answers])

    def create_votes(self, num_votes, users, questions, answers, batch_size):
        # 1. Подготовка ID
        user_ids = [u.id for u in users]
        answer_ids = [a.id for a in answers]

        # 2. Проверка на пустые списки
        if not user_ids or not answer_ids:
            self.stdout.write(self.style.WARNING('   Нет пользователей или ответов'))
            return 0

        # 3. Расчет лимитов
        max_possible = len(user_ids) * len(answer_ids)
        votes_to_create = min(num_votes // 2, max_possible)

        if votes_to_create <= 0:
            self.stdout.write(self.style.WARNING('   Нет голосов для создания'))
            return 0

        self.stdout.write(f'   Генерация {votes_to_create} голосов...')

        # Сценарий А: Заполнить ВСЕ возможные комбинации
        if votes_to_create == max_possible:
            votes = []
            for uid in user_ids:
                for aid in answer_ids:
                    votes.append(Vote(
                        user_id=uid,
                        answer_id=aid,
                        vote_value=random.choice([1, -1])
                    ))
                    if len(votes) >= batch_size:
                        Vote.objects.bulk_create(votes, ignore_conflicts=True)
                        votes = []
            if votes:
                Vote.objects.bulk_create(votes, ignore_conflicts=True)
            return votes_to_create

        # Сценарий Б: Выборочное заполнение
        used_pairs = set()
        votes = []

        for i in range(votes_to_create):
            # Поиск уникальной пары (оптимизированный random)
            while True:
                uid = user_ids[random.randint(0, len(user_ids) - 1)]
                aid = answer_ids[random.randint(0, len(answer_ids) - 1)]
                pair = (uid, aid)
                if pair not in used_pairs:
                    used_pairs.add(pair)
                    break

            votes.append(Vote(
                user_id=uid,
                answer_id=aid,
                vote_value=random.choice([1, -1])
            ))

            # Сброс батча
            if len(votes) >= batch_size:
                Vote.objects.bulk_create(votes, ignore_conflicts=True)
                votes = []

                # Очистка set при большом объеме
                if len(used_pairs) > 5_000_000:
                    used_pairs.clear()

        # Запись остатков
        if votes:
            Vote.objects.bulk_create(votes, ignore_conflicts=True)

        return votes_to_create

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