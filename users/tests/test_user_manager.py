import pytest
from django.conf import settings
from django.core import exceptions

from entropy import password_hashers
from entropy.errors import messages

user_model = settings.AUTH_USER_MODEL


@pytest.mark.django_db
class TestUserManagerPositive:
    """
    Positive tests on user's manager.
    """

    def test_create_user(self, user_initial_data: dict, django_user_model: user_model):
        """
        Check that user manager's method 'create_user' provided with correct set of data
        successfully creates new user model's instance and saves it in DB.
        """
        new_user_instance = django_user_model.objects.create_user(**user_initial_data)

        assert django_user_model.objects.filter(email=user_initial_data['email']).exists()
        assert new_user_instance.password.startswith(
            password_hashers.CustomArgon2PasswordHasher.algorithm
        )

    def test_create_superuser(self, user_initial_data: dict, django_user_model: user_model):
        """
        Check that user manager's method 'create_superuser' provided with correct set of data
        successfully creates new user model's instance with a 'is_superuser' flag = True and saves it in DB.
        """
        user_initial_data['is_superuser'] = True
        django_user_model.objects.create_superuser(**user_initial_data)

        assert django_user_model.objects.filter(
            email=user_initial_data['email'],
            is_superuser=True,
                ).exists()

    def test_validate_raw_password(self, user_initial_data: dict, django_user_model: user_model):
        """
        Check that if correct raw password is provided - than validation error would
        not be raiser.
        """
        good_password = 'rkgrt4Hp65'
        user = django_user_model(**user_initial_data)

        assert django_user_model.objects.validate_raw_password(good_password, user) is None


@pytest.mark.django_db
class TestUserManagerNegative:
    """
    Positive tests on user's manager.
    """
    def test_validate_raw_password(self, user_initial_data: dict, django_user_model: user_model):
        """
        Check that if incorrect raw password is provided - than validation error would
        be raiser.
        """
        bad_password = '1111'
        user = django_user_model(**user_initial_data)

        with pytest.raises(exceptions.ValidationError, match=str(messages.user_3)):
            django_user_model.objects.validate_raw_password(bad_password, user)


