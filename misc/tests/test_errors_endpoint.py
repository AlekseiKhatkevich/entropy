from rest_framework import status
from rest_framework.reverse import reverse

from entropy.errors import messages


class TestErrorsEndpointPositive:
    """
    Positive tests on /misc/errors/ GET endpoint.
    """
    def test_response(self, client):
        """
        Check response status and response content.
        """
        errors = [msg for msg in vars(messages).values() if isinstance(msg, messages.ErrorMessage)]

        response = client.get(
            reverse('errors'),
            data=None,
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(errors)

        sample_error = response.data[0]
        sample_error_class = getattr(messages, sample_error['error_code'])

        for field, value in sample_error.items():
            assert value == getattr(sample_error_class, field)