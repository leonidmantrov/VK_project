from django.apps import AppConfig


class VkstartConfig(AppConfig):
    name = 'questions'

    def ready(self):
        import questions.signals