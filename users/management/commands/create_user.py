from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Create a user with custom fields'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email address of the user')
        parser.add_argument('password', type=str, help='Password of the user')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']

        user = User.objects.create(
            email=email,
            is_superuser=False,
            is_staff=False,
        )
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created user with email: {email}'))
