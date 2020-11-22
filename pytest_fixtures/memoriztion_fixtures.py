import pytest
from django.db import transaction
from typing import Callable

from memorization.models import Word

LANGUAGES = {
    'russian': {
        'name': 'Дом',
        'definition': 'Здание, строение, предназначенное для жилья, для размещения различных учреждений и предприятий.',
        'language_id': 'ru',
    },
    'english': {
        'name': 'home',
        'definition': 'the place where one lives permanently, especially as a member of a family or household.',
        'language_id': 'en',
    },
    'spanish': {
        'name': 'casa',
        'definition': 'Una casa es un edificio para habitar.',
        'language_id': 'es',
    },
    'polish': {
        'name': 'mieszkanie',
        'definition': 'mieszkaniem jest zespół pomieszczeń mieszkalnych i pomocniczych mający odrębne wejście',
        'language_id': 'pl',
    }}


@pytest.fixture(scope='function')
def one_word(request) -> Callable:
    """
    Creates Word model instance in chosen language.
    language - language from list at the top of the module.
    save_to_db - whether instance saved to db or not.
    """

    def _closure(language: str, save_to_db: bool = False) -> Word:
        instance = Word(**LANGUAGES[language])
        if save_to_db:
            instance.save()

        return instance

    yield _closure


@pytest.fixture(scope='module')
def one_word_with_translations(django_db_setup, django_db_blocker) -> list[Word]:
    """
    Creates few test words and joins them in one group by translation.
    """
    with django_db_blocker.unblock():
        with transaction.atomic():
            instances = Word.objects.bulk_create(
                Word(**language) for language in LANGUAGES.values()
            )
            instance_1, *rest = instances
            instance_1.translation.add(*rest)

        yield instances

        pks = [instance.pk for instance in instances]
        Word.objects.filter(pk__in=pks).delete()
