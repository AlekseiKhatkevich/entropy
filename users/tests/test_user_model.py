from uuid import UUID

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError


@pytest.fixture(scope='function')
def user_initial_data():
    initial_data = dict(
        email='test@email.com',
        password='argon2id$argon2i$v=19$m=512,t=2,p=2$SDV5RzU4eG5OcWU0$o1+GMGzgCYNOi8fBTqgmYQ',
        nickname='testuser',
        timezone='Iceland',
    )
    return initial_data


@pytest.mark.django_db
class TestUserModelPositive:
    """
    Positive test on User model
    """
    def test_model_creation(self, user_initial_data):
        """
        Check that if correct data is provided, then User model instance can be created.
        """
        user = get_user_model().objects.create(**user_initial_data)

        assert get_user_model().objects.filter(**user_initial_data).exists()

        assert UUID(str(user.id), version=4)


@pytest.mark.django_db
class TestUserModelNegative:
    """
    Negative test on User model
    """
    def test_timezone_check(self, user_initial_data):
        """
        Check that check constraint 'timezone_check' does not allow to save
        a timezone with incorrect name in DB.
        """
        user_initial_data['timezone'] = 'Narnia'
        expected_error_message = 'timezone_check'

        with pytest.raises(IntegrityError, match=expected_error_message):
            get_user_model().objects.create(fc=False, **user_initial_data)

    def test_argon2_hash_check(self, user_initial_data):
        """
        Check that check constraint 'argon2_hash_check' does not allow to save
        a non - Argon2 style password hash to DB.
        """
        user_initial_data['password'] = 'abracadabra'
        expected_error_message = 'argon2_hash_check'

        with pytest.raises(IntegrityError, match=expected_error_message):
            get_user_model().objects.create(fc=False, **user_initial_data)
