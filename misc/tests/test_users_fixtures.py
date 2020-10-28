from typing import Callable

import pytest
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

user = settings.AUTH_USER_MODEL


class TestUsersFixturesPositive:
    """
    Positive tests on users app fixtures
    """
    def test_user_initial_data_fixture(self, user_initial_data: dict):
        """
        Check that 'user_initial_data' fixture returns dict with initial user's data.
        """
        fields_in_data = {'email', 'password', 'nickname', 'timezone', }
        assert isinstance(user_initial_data, dict)
        assert fields_in_data == user_initial_data.keys()

    def test_jwt_auth_header_fixture(self, one_test_user: user, jwt_auth_header: Callable):
        """
        Check that fixture 'jwt_auth_header' returns a callable which in turn returns
        dict with 'HTTP_AUTHORIZATION' header mapped to JWT access token.
        """
        header = jwt_auth_header(one_test_user)
        backend = JWTAuthentication()
        _, token = header['HTTP_AUTHORIZATION'].split(' ')
        decrypted_token = backend.get_validated_token(token)

        assert callable(jwt_auth_header)
        assert isinstance(header, dict)
        assert decrypted_token['user_id'] == str(one_test_user.pk)

    @pytest.mark.django_db
    def test_one_test_user_fixture(self, one_test_user: user, django_user_model: user):
        """
        Check that 'one_test_user' fixture creates one test user instance and saves it in DB.
        """
        assert django_user_model.objects.filter(email=one_test_user.email).exists()
        assert hasattr(one_test_user, 'jwt_auth_header')


