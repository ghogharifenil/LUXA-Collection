from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    User = get_user_model()

    email = getattr(settings, "ADMIN_EMAIL", None)
    password = getattr(settings, "ADMIN_PASSWORD", None)
    name = getattr(settings, "ADMIN_NAME", "Fenil")
    city = getattr(settings, "ADMIN_CITY", "Surat")

    if not email or not password:
        return

    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(
            email=email,
            name=name,
            city=city,
            password=password
        )