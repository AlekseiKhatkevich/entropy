import uuid
import zoneinfo

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.db.models import Q

from entropy import validators as project_validators
from users.managers import UserManager


class User(AbstractBaseUser):
    """
    Custom user model
    """
    USERNAME_FIELD = EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('password', )

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
    password = models.CharField(
        verbose_name='password',
        max_length=128,
        validators=[
            project_validators.Argon2HashValidator()
        ]
    )
    registration_date = models.DateTimeField(
        verbose_name='User registration date',
        auto_now_add=True,
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
        unique=True,
    )
    timezone = models.CharField(
        verbose_name='User timezone',
        max_length=50,
        null=True,
        blank=True,
        validators=[
            project_validators.TimeZoneValidator(),
        ]
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = (
            models.CheckConstraint(
                name='timezone_check',
                check=Q(timezone__in=zoneinfo.available_timezones())
            ),
            models.CheckConstraint(
                name='argon2_hash_check',
                check=Q(
                    password__length=project_validators.Argon2HashValidator.standard_hash_len,
                    password__startswith=project_validators.Argon2HashValidator.hash_prefix,
                )
            )
        )
        indexes = (
            BrinIndex(fields=('registration_date', ), autosummarize=True,),
        )

    def save(self, fc=True, *args, **kwargs):
        if fc:
            self.full_clean()
        super().save(*args, **kwargs)








