import pytest
from django.core import exceptions
from django.db import IntegrityError
from django.utils import timezone

from entropy.errors import messages
from memorization.models import NoteBook


@pytest.mark.django_db
class TestNotebookModelPositive:
    """
    Positive tests on 'Notebook' model.
    """
    def test_create_model_instance(self, one_test_user, one_word_with_translations):
        """
        Check whether it's possible to create one model instance provided that
        correct set of input data has been supplied.
        """
        positive_data = dict(
            user=one_test_user,
            word=one_word_with_translations[0],
            learn_in_language_id='pt',
        )
        NoteBook.objects.create(**positive_data)

        assert NoteBook.objects.filter(**positive_data).exists()


@pytest.mark.django_db
class TestNotebookModelNegative:
    """
    Negative tests on 'Notebook' model.
    """
    def test_clean_learn_in_language(self, one_test_user, one_word):
        """
        Check if 'learn_in_language' field equal to language of 'word' field, then Validation error
        would be arisen.
        """
        negative_data = dict(
            user=one_test_user,
            word=one_word('russian'),
            learn_in_language_id='ru',
        )
        expected_error_message = str(messages.memo_notebook_1)
        expected_exception = exceptions.ValidationError

        with pytest.raises(expected_exception, match=expected_error_message):
            NoteBook.objects.create(**negative_data)

    def test_clean_entry_date_lt_memorization_date(self, one_test_user, one_word):
        """
        Check if 'entry_date' field is greater than 'memorization_date' field - Validation error
        would be arisen.
        """
        negative_data = dict(
            user=one_test_user,
            word=one_word('russian'),
            learn_in_language_id='en',
            memorization_date=timezone.now() - timezone.timedelta(days=1),
        )
        expected_error_message = str(messages.memo_notebook_2)
        expected_exception = exceptions.ValidationError

        with pytest.raises(expected_exception, match=expected_error_message):
            NoteBook.objects.create(**negative_data)

    def test_entry_date_vs_memorization_date_check_constraint(self, one_test_user, one_word):
        """
        Check 'entry_date_vs_memorization_date_check' constraint.
        """
        negative_data = dict(
            user=one_test_user,
            word=one_word('russian'),
            learn_in_language_id='en',
            memorization_date=timezone.now() - timezone.timedelta(days=1),
        )
        expected_error_message = 'entry_date_vs_memorization_date_check'
        expected_exception = IntegrityError

        with pytest.raises(expected_exception, match=expected_error_message):
            instance = NoteBook(**negative_data)
            instance.save(fc=False)