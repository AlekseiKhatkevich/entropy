from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """
    Adds 'user_id' attribute to request.
    """

    def authenticate(self, request):
        user_and_token = super().authenticate(request)

        if user_and_token is not None:
            user, token = user_and_token
            request.user_id = user.pk

        return user_and_token
