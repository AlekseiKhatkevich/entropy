import pytest
from memorization.models import Word


@pytest.mark.django_db
class TestWordPositive:
    """
    Positive tests on 'Word' model.
    """
    def test_create_one_word(self, one_word_with_translations):
        """
        Check whether possible to create one 'Word' model instance provided that correct
        set of input data has supplied.
        """
        positive_data = dict(
            name='haus',
            definition='test',
            language_id='de',
        )
        new_word = Word.objects.create(**positive_data)
        new_word.translation.set(one_word_with_translations)