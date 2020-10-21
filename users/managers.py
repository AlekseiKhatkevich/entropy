from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db.models import Model
from entropy.errors import messages


class UserManager(BaseUserManager):
    """
    Manager for User model
    """
    def create_user(self, email: str, password: str, **extra_fields) -> Model:
        """
        Create and save a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        self.validate_raw_password(password, user)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> Model:
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields['is_superuser'] = True

        return self.create_user(email, password, **extra_fields)

    @staticmethod
    def validate_raw_password(password: str, user: Model) -> None:
        """
        Validates raw user password against AUTH_PASSWORD_VALIDATORS
        :param password: raw password string
        :param user: User model instance
        :return: None
        """
        try:
            validate_password(password, user)
        except exceptions.ValidationError as err:
            raise exceptions.ValidationError(
                *messages.user_3,
                params=str(err),
            ) from err
