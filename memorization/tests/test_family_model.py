import pytest
from django.core import exceptions
from django.db import IntegrityError
from django.db.models.query import QuerySet

from entropy.errors import messages
from memorization.models import Family, Language


@pytest.fixture(scope='module')
def languages() -> QuerySet:
    """
    Returns queryset with a pair of language objects chosen randomly.
    """
    return Language.objects.order_by('?')[:2]


@pytest.mark.django_db
class TestFamilyModelPositive:
    """
    Positive tests on 'entropy' app 'Family' model.
    """
    def test_create_model_instance(self, languages):
        """
        Check that providing correct input data it is possible successfully create
        'Family' model instance.
        """
        language_group_name = 'test'
        language_1, language_2 = languages
        language_1.family.add(language_2, through_defaults={'name': language_group_name})

        assert Family.objects.filter(
            first_language=language_1,
            second_language=language_2,
            name=language_group_name,
        ).exists()


@pytest.mark.django_db
class TestFamilyModelNegative:
    """
    Negative tests on 'entropy' app 'Family' model.
    """
    def test_point_on_itself_check(self, languages):
        """
        Check 'point_on_itself_check' would not allow saving in DB 'Family' model instance
        where first_language is equal to second_language.
        """
        expected_error_message = 'point_on_itself_check'

        with pytest.raises(IntegrityError, match=expected_error_message):
            language, _ = languages
            language.family.add(language)

    def test_clean_first_language_ne_second_language(self, languages):
        """
        Check if 'clean' method in 'Family' model would raise an exception
        in case first_language is equal to second_language.
        """
        expected_error_message = messages.memo_family_1
        language, _ = languages

        with pytest.raises(exceptions.ValidationError, match=str(expected_error_message)):
            Family.objects.create(first_language=language, second_language=language)

