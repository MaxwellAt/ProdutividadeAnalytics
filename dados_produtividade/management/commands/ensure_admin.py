from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates a superuser (admin/admin) if it does not exist.'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin'

        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"User '{username}' does not exist. Creating..."))
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f"Superuser created!\nUsername: {username}\nPassword: {password}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists."))
