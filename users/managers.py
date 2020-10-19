from django.contrib.auth.models import BaseUserManager
from django.db.models import Model


class UserManager(BaseUserManager):
    """
    Manager for User model
    """
    def create_user(self, email: str, password: str, **extra_fields) -> Model:
        """
        Create and save a User with the given email and password.
        """
        mandatory_fields = (email, password,)
        if not all(mandatory_fields):
            raise ValueError('Email and password must be specified')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> Model:
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields['is_superuser'] = True

        return self.create_user(email, password, **extra_fields)