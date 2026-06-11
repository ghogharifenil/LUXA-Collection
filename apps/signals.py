import os
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    User = get_user_model()

    email = os.environ.get("ADMIN_EMAIL")
    password = os.environ.get("ADMIN_PASSWORD")
    name = os.environ.get("ADMIN_NAME", "Fenil")
    city = os.environ.get("ADMIN_CITY", "Surat")

    if not email or not password:
        return

    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(
            email=email,
            name=name,
            city=city,
            password=password
        )