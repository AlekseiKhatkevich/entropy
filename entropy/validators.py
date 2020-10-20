import zoneinfo

from django.core import exceptions
from django.utils.deconstruct import deconstructible


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
                'timezone name is incorrect'
            ) from err
