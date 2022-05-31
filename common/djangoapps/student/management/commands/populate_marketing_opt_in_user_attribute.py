""" Management command to back-populate marketing emails opt-in for the user accounts. """

import time

from django.contrib.auth.models import User  # lint-amnesty, pylint: disable=imported-auth-user
from django.core.management.base import BaseCommand

from common.djangoapps.student.models import UserAttribute

MARKETING_EMAILS_OPT_IN = 'marketing_emails_opt_in'


class Command(BaseCommand):
    """
    Example usage:
        $ ./manage.py lms populate_marketing_opt_in_user_attribute
    """
    help = """
        Creates a row in the UserAttribute table for all users in the platform.
        This command back-populates the 'marketing_emails_opt_in' attribute in the
        UserAttribute table for the user accounts.
        """

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-delay',
            type=float,
            dest='batch_delay',
            default=1.0,
            help='Time delay in each iteration'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            dest='batch_size',
            default=5000,
            help='Batch size'
        )

    def handle(self, *args, **options):
        """
        This command back-populates the 'marketing_emails_opt_in' attribute for all existing users who do not already
        have the attribute set.
        """
        def get_user_queryset():
            return User.objects.order_by('id')[offset: offset + batch_size]

        offset = 0
        count = User.objects.count()
        batch_delay = options['batch_delay']
        batch_size = options['batch_size']

        self.stdout.write(f'Command execution started with options: {options}.')

        while offset < count:
            self.stdout.write(f'Back filling user attribute in batch from {offset} to {offset + batch_size}')

            users = get_user_queryset()
            for user in users:
                if not UserAttribute.get_user_attribute(user, MARKETING_EMAILS_OPT_IN):
                    UserAttribute.set_user_attribute(user, MARKETING_EMAILS_OPT_IN, str(user.is_active).lower())
            offset += batch_size
            time.sleep(batch_delay)

        self.stdout.write('Command executed successfully.')
