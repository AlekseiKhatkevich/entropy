import pytest
from django.conf import settings


user_model = settings.AUTH_USER_MODEL


@pytest.fixture(scope='function')
def user_initial_data() -> dict:
    """
    Creates positive initial data for user instance creation.
    :return: dict with user's data
    """
    initial_data = dict(
        email='test@email.com',
        password='rkgrt4Hp65',
        nickname='testuser',
        timezone='Iceland',
    )

    return initial_data


@pytest.fixture(scope='function')
def one_test_user(django_user_model: user_model, user_initial_data: dict) -> user_model:
    """
    Creates one single user entry
    :param django_user_model: user model
    :param user_initial_data: dictionary with user initial data
    :return: one user model instance
    """
    user = django_user_model.objects.create_user(**user_initial_data)

    return user
