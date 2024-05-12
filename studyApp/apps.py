from django.apps import AppConfig


class StudyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'studyApp'

    def ready(self):
        # Import and connect signals here
        from . import signals
