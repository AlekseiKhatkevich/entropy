from typing import Callable

import pytest
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

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
def jwt_auth_header() -> Callable:
    """
    Returns jwt_auth_header: 'HTTP_AUTHORIZATION' Bearer {token} HTTP header
    """
    def _wrapper(user: user_model) -> dict:
        refresh = RefreshToken.for_user(user)
        jwt_auth_header = {
            'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}',
        }
        return jwt_auth_header

    return _wrapper


@pytest.fixture(scope='function')
def one_test_user(django_user_model: user_model,
                  user_initial_data: dict,
                  jwt_auth_header: Callable,
                  ) -> user_model:
    """
    Creates one single user entry + jwt token pair for authentication.
    :param jwt_auth_header: callable that produces header: 'HTTP_AUTHORIZATION'
    :param django_user_model: user model
    :param user_initial_data: dictionary with user initial data
    :return: one user model instance
    """
    user = django_user_model.objects.create_user(**user_initial_data)
    user.jwt_auth_header = jwt_auth_header(user)

    return user
