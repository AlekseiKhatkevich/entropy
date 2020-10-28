import pytest
from django.conf import settings
from django.test.client import Client
from rest_framework import status
from rest_framework.reverse import reverse

user = settings.AUTH_USER_MODEL


@pytest.mark.django_db
class TestMePositive:
    """
    Positive tests on Djoser /users/me/ api endpoint.
    """

    def test_detail_action(self, one_test_user: user, client: Client):
        """
        Check that following fields are present in response:
            'nickname'
            'timezone'
            'registration_date'
            'last_change'
            'is_superuser'
        """
        extra_fields = {
            'nickname',
            'timezone',
            'registration_date',
            'last_change',
            'is_superuser',
        }

        response = client.get(
            reverse('user-me'),
            data=None,
            **one_test_user.jwt_auth_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert extra_fields.issubset(response.data.keys())

    def test_update_action(self, one_test_user: user, client: Client, django_user_model: user):
        """
        Check that it is possible to change following fields on PUT and PATCH action.
            'nickname'
            'timezone'
        """
        data = dict(
            timezone='UTC',
            nickname='test-me-action',
        )
        response = client.put(
            reverse('user-me'),
            data=data,
            content_type='application/json',
            ** one_test_user.jwt_auth_header,
        )

        assert response.status_code == status.HTTP_200_OK
        assert django_user_model.objects.filter(email=one_test_user.email, **data).exists()

