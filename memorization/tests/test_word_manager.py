import pytest
from memorization.models import Word


@pytest.mark.django_db
class TestWordManagerPositive:
    """
    Positive tests on 'Word' model manager in 'memorization' app.
    """
    @pytest.fixture(scope='function')
    def linked_words(self, one_word, db):
        self.russian_word = one_word('russian', save_to_db=True)
        self.english_word = one_word('english', save_to_db=True)
        self.spanish_word = one_word('spanish', save_to_db=True)
        self.polish_word = one_word('polish', save_to_db=True)

        self.russian_word.translation.add(self.english_word)
        self.english_word.translation.add(self.spanish_word)

    def test_word_translations(self, linked_words):
        """
        Check whether method would return instances of linked words (linked via translation m2m).
        """

        words = Word.objects.word_translations(self.russian_word.pk)

        assert self.english_word in words
        assert self.spanish_word in words
        assert len(words) == 2

    def test_word_translation_limited_by_language(self, linked_words):
        """
        Check whether method would return instances of linked words  limited by language.
        """
        words = Word.objects.word_translations(self.russian_word.pk, ('es',))

        assert self.spanish_word in words
        assert len(words) == 1