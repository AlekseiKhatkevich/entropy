import zoneinfo

import pytest
from django.core import exceptions
from django.utils import timezone

from entropy import validators
from entropy.errors import messages


class TestValidatorsPositive:
    """
    Positive tests on custom validators.
    """
    def test_TimeZoneValidator(self):
        """
        Check that if 'TimeZoneValidator' receives correct timezone name - validation error would not
        be raised.
        """
        validator = validators.TimeZoneValidator()
        correct_timezone_name = zoneinfo.available_timezones().pop()

        validator(correct_timezone_name)

    def test_Argon2HashValidator(self):
        """
        Check that 'Argon2HashValidator' would not raise validation error in case correct
        argon2 style hash is provided.
        """
        validator = validators.Argon2HashValidator()
        correct_hash = 'argon2id$argon2i$v=19$m=512,t=2,p=2$SDV5RzU4eG5OcWU0$o1+GMGzgCYNOi8fBTqgmYQ'

        validator(correct_hash)

    def test_ProtectFutureValidator(self):
        """
        Check 'ProtectFutureValidator' raises Validation error in case value (datetime) is in the future.
        Not in this case as it is a positive test.
        """
        expected_error_message = messages.memo_notebook_4
        validator = validators.ProtectFutureValidator(
            message=str(expected_error_message),
            code=expected_error_message.error_code,
        )

        validator(timezone.now())


class TestValidatorsNegative:
    """
    Positive tests on custom validators.
    """

    def test_TimeZoneValidator(self):
        """
        Check that if 'TimeZoneValidator' receives incorrect timezone name - validation error would
        be raised.
        """
        validator = validators.TimeZoneValidator()
        incorrect_timezone_name = 'Narnia'
        expected_error_message = str(messages.user_2)

        with pytest.raises(exceptions.ValidationError, match=expected_error_message):
            validator(incorrect_timezone_name)

    def test_Argon2HashValidator(self):
        """
        Check that 'Argon2HashValidator' would raise validation error in case incorrect
        argon2 style hash is provided.
        """
        validator = validators.Argon2HashValidator()
        incorrect_hash = 'abracadabra'
        expected_error_message = str(messages.user_4)

        with pytest.raises(exceptions.ValidationError, match=expected_error_message):
            validator(incorrect_hash)

    def test_ProtectFutureValidator(self):
        """
        Check 'ProtectFutureValidator' raises Validation error in case value (datetime) is in the future.
        """
        expected_error_message = expected_error_message = messages.memo_notebook_4
        expected_exception = exceptions.ValidationError,
        validator = validators.ProtectFutureValidator(
            message=str(expected_error_message),
            code=expected_error_message.error_code,
        )

        with pytest.raises(expected_exception, match=str(expected_error_message)):
            validator(timezone.now() + timezone.timedelta(days=1))