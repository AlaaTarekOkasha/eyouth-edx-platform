"""
Unittests for populate_marketing_opt_in_user_attribute management command.
"""

import pytest
from django.contrib.auth.models import User  # lint-amnesty, pylint: disable=imported-auth-user
from django.core.management import call_command
from django.test import TestCase

from common.djangoapps.student.models import UserAttribute
from common.djangoapps.student.tests.factories import UserFactory
from openedx.core.djangolib.testing.utils import skip_unless_lms

MARKETING_EMAILS_OPT_IN = 'marketing_emails_opt_in'


@skip_unless_lms
class TestPopulateMarketingOptInUserAttribute(TestCase):
    """
    Test populate_marketing_opt_in_user_attribute management command.
    """

    def setUp(self):
        super().setUp()
        self.existing_user = UserFactory()

    def test_command_with_existing_users(self):
        """
        Test population of marketing_emails_opt_in attribute with an existing user.
        """
        assert UserAttribute.objects.count() == 0
        call_command('populate_marketing_opt_in_user_attribute')
        assert UserAttribute.objects.filter(name=MARKETING_EMAILS_OPT_IN).count() == User.objects.count()

    def test_command_with_new_user(self):
        """
        Test population of marketing_emails_opt_in attribute with a new user.
        """
        user = UserFactory()
        call_command('populate_marketing_opt_in_user_attribute')
        assert UserAttribute.objects.filter(name=MARKETING_EMAILS_OPT_IN).count() == User.objects.count()

    def test_command_with_invalid_argument(self):
        """
        Test management command raises TypeError on wrong data type value for '--batch-size' argument.
        """
        with pytest.raises(TypeError):
            call_command(
                "populate_marketing_opt_in_user_attribute",
                batch_size='1000'
            )
