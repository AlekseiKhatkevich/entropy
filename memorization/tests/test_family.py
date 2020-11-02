import pytest
from memorization.models import Family, Language

latin = ('es', 'pt', 'it', 'fr', )
slavic = ('ru', 'uk', 'be', )
german = ('de', 'nl', )


@pytest.mark.django_db
class TestFamilyPositive:
    """
    Positive tests on 'Family' model
    """
    def test_create_family(self):
        latin_languages = Language.objects.filter(code__in=latin)
        spanish, *rest = latin_languages
        spanish.family.add(*rest, through_defaults={'name': 'test'})

        family = Family.objects.all()
        first_languages_id = {language.first_language_id for language in family}
        second_languages_id = {language.second_language_id for language in family}

        assert first_languages_id == first_languages_id
        assert len(first_languages_id) == len(second_languages_id) == len(latin)

        latin_languages_ids = {language.pk for language in latin_languages}

        assert latin_languages_ids == first_languages_id == first_languages_id


@pytest.mark.django_db
class TestFamilyNegative:
    """
    Negative tests on 'Family' model
    """