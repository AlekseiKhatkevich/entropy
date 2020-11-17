import pytest
from django.db import transaction

from memorization.models import Word

russian = (
        'Дом',
        'Здание, строение, предназначенное для жилья, для размещения различных учреждений и предприятий.',
        'ru',
    )
english = (
        'home',
        'the place where one lives permanently, especially as a member of a family or household.',
        'en',
    )
spanish = (
        'casa',
        'Una casa es un edificio para habitar.',
        'es',
    )


@pytest.fixture(scope='module')
def one_word_with_translations(django_db_setup, django_db_blocker) -> list[Word]:
    """
    Creates few test words and joins them in one group by translation.
    """
    def _one_word_instance(name, definition, language):
        instance = Word(
            name=name,
            definition=definition,
            language_id=language,
        )
        return instance

    with django_db_blocker.unblock():
        with transaction.atomic():
            instances = Word.objects.bulk_create(
                _one_word_instance(*language) for language in (russian, english, spanish)
            )
            instance_1, *rest = instances
            instance_1.translation.add(*rest)

        yield instances

        pks = [instance.pk for instance in instances]
        Word.objects.filter(pk__in=pks).delete()






