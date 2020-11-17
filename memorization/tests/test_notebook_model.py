import pytest
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
