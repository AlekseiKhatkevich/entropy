from uuid import UUID

import pytest
from django.conf import settings
from django.db import IntegrityError

user_model = settings.AUTH_USER_MODEL


@pytest.mark.django_db
class TestUserModelPositive:
    """
    Positive test on User model
    """

    def test_model_creation(
            self,
            django_user_model: user_model,
            user_initial_data: dict,
    ):
        """
        Check that if correct data is provided, then User model instance can be created.
        """
        user = django_user_model(**user_initial_data)
        user.set_password(user.password)
        user.save()

        assert django_user_model.objects.filter(email=user_initial_data['email']).exists()

        assert UUID(str(user.id), version=4)


@pytest.mark.django_db
class TestUserModelNegative:
    """
    Negative test on User model
    """

    def test_timezone_check(
            self,
            django_user_model: user_model,
            user_initial_data: dict,
    ):
        """
        Check that check constraint 'timezone_check' does not allow to save
        a timezone with incorrect name in DB.
        """
        user_initial_data['timezone'] = 'Narnia'
        expected_error_message = 'timezone_check'

        with pytest.raises(IntegrityError, match=expected_error_message):
            user = django_user_model(**user_initial_data)
            user.set_password(user.password)
            user.save(fc=False)

    def test_argon2_hash_check(
            self,
            django_user_model: user_model,
            user_initial_data: dict,
    ):
        """
        Check that check constraint 'argon2_hash_check' does not allow to save
        a non - Argon2 style password hash to DB.
        """
        user_initial_data['password'] = 'abracadabra'
        expected_error_message = 'argon2_hash_check'

        with pytest.raises(IntegrityError, match=expected_error_message):
            user = django_user_model(**user_initial_data)
            user.save(fc=False)
