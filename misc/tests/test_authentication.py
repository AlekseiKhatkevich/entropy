from rest_framework.test import APIRequestFactory

from entropy.authentication import CustomJWTAuthentication


class TestCustomAuthentication:
    """
    Positive test on CustomJWTAuthentication backend.
    """
    def test_backend_sets_user_id(self, one_test_user):
        """
        Check that CustomJWTAuthentication backend would set request.user_id attribute
        with user_id of successfully authenticated user.
        """
        backend = CustomJWTAuthentication()
        factory = APIRequestFactory()
        request = factory.post(
            '/test/',
            {'test': 'test'},
            content_type='application/json',
            **one_test_user.jwt_auth_header,
        )

        backend.authenticate(request)

        assert request.user_id == one_test_user.pk