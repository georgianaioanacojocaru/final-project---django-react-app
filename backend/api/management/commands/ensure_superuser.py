import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import environ

env = environ.Env()
environ.Env.read_env()

class Command(BaseCommand):
    help = """Creates an admin user non-interactively if it doesn't exist

    Provide the following required environment variables:
    DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD
    """

    def handle(self, *_args, **_kwargs):
        User = get_user_model()

        email = os.environ["DJANGO_SUPERUSER_EMAIL"]
        password = os.environ["DJANGO_SUPERUSER_PASSWORD"]

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser( email=email, password=password)  # type: ignore
            self.stdout.write(self.style.SUCCESS(f"The superuser '{email}' was created successfully"))
