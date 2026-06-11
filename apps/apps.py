from django.apps import AppConfig

class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if not User.objects.filter(email="admin@gmail.com").exists():
            User.objects.create_superuser(
                email="ghogharifenil601@gmail.com",
                name="Fenil",
                city="Surat",
                password="0121"
            )