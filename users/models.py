from django.db import models
import uuid


class User(models.Model):
    """
    Custom user model
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    #objects =

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
    is_staff = models.BooleanField(
        verbose_name='Is user staff?',
        default=False,
    )
    nickname = models.CharField(
        verbose_name='User nickname',
        max_length=30,
        null=True,
        blank=True,
    )

    class Meta:
        pass

    def __str__(self):
        pass



