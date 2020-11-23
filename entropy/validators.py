import zoneinfo
from django.utils import timezone
from django.core import exceptions
from django.utils.deconstruct import deconstructible

from entropy.errors import messages


@deconstructible
class ProtectFutureValidator:
    """
    Validates if date is in the future or not. If so - raises an exception.
    """

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __call__(self, value):
        assert timezone.is_aware(value), 'Datetime should be aware.'

        if value > timezone.now():
            raise exceptions.ValidationError(
                self.message,
                self.code,
            )


@deconstructible
class TimeZoneValidator:
    """
    Validates whether input string is valid timezone name or not.
    """

    def __call__(self, value):
        try:
            zoneinfo.ZoneInfo(value)
        except zoneinfo.ZoneInfoNotFoundError as err:
            raise exceptions.ValidationError(
                *messages.user_2,
            ) from err


@deconstructible
class Argon2HashValidator:
    """
    Validates whether a given string looks like argon2id hash or not.
    example - argon2id$argon2i$v=19$m=512,t=2,p=2$SDV5RzU4eG5OcWU0$o1+GMGzgCYNOi8fBTqgmYQ
    """
    standard_hash_len = 75
    hash_prefix = 'argon2id'

    def __call__(self, value):
        startswith_argon2id = value.startswith(self.hash_prefix)
        hash_len = len(value) == self.standard_hash_len

        if not (startswith_argon2id and hash_len):
            raise exceptions.ValidationError(
                *messages.user_4,
            )
