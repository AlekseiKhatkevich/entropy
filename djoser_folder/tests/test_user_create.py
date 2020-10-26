import pytest
from django.conf import settings
from django.test.client import Client
from rest_framework import status
from rest_framework.reverse import reverse

user = settings.AUTH_USER_MODEL


@pytest.mark.django_db
def test_user_create_positive(
        user_initial_data: dict,
        client: Client,
        django_user_model: user
):
    """
    Check that during user creation via Djoser api endpoint /auth/users/:POST it is possible
    to specify 'nickname' and 'timezone' fields as well. They are bot not required.
    """
    response = client.post(
        reverse('user-list'),
        data=user_initial_data,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response['Content-Type'] == 'application/json'
    assert django_user_model.objects.filter(pk=response.data['id']).exists()
    assert {'timezone', 'nickname', }.issubset(response.data.keys())




