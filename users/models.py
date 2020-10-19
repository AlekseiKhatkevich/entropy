import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from users.managers import UserManager


class User(AbstractBaseUser):
    """
    Custom user model
    """
    USERNAME_FIELD = EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password', ]

    last_login = None

    objects = UserManager()

    id = models.UUIDField(
        verbose_name='User id (UID)',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        verbose_name='User email',
        unique=True,
    )
    registration_date = models.DateTimeField(
        verbose_name='User registration date',
        auto_now_add=True
    )
    last_change = models.DateTimeField(
        verbose_name='Last time user model has changed',
        auto_now=True,
    )
    is_superuser = models.BooleanField(
        verbose_name='Is user superuser',
        default=False,
    )
    nickname = models.CharField(
        verbose_name='User nickname',
        max_length=30,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'





