from django import forms
from .models import Question, Tag


class QuestionForm(forms.ModelForm):
    tags_input = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['title_question', 'question_text']

    def clean_title_question(self):
        title = self.cleaned_data.get('title_question', '').strip()

        if len(title) < 10:
            raise forms.ValidationError('Заголовок должен содержать минимум 10 символов')

        return title

    def clean_question_text(self):
        text = self.cleaned_data.get('question_text', '').strip()

        if len(text) < 20:
            raise forms.ValidationError('Текст вопроса должен содержать минимум 20 символов')

        return text

    def clean_tags_input(self):
        tags_input = self.cleaned_data.get('tags_input', '')

        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

            if len(tags) > 5:
                raise forms.ValidationError('Максимум 5 тегов')

            for tag in tags:
                if len(tag) > 50:
                    raise forms.ValidationError(f'Тег "{tag[:20]}..." слишком длинный (макс. 50 символов)')

                import re
                if re.search(r'[<>{}[\]]', tag):
                    raise forms.ValidationError(f'Тег "{tag}" содержит запрещенные символы')

            lower_tags = [t.lower() for t in tags]
            if len(lower_tags) != len(set(lower_tags)):
                raise forms.ValidationError('Теги не должны повторяться')

        return tags_input

    def save(self, commit=True):
        question = super().save(commit=False)
        if self.user:
            question.user = self.user

        if commit:
            question.save()
            self.save_tags(question)

        return question

    def save_tags(self, question):
        tags_input = self.cleaned_data.get('tags_input', '')
        if tags_input:
            for tag_name in tags_input.split(','):
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(tag_text=tag_name)
                    question.tags.add(tag)