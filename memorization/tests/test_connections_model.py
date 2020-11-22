import pytest
from django.core import exceptions
from django.db import IntegrityError

from entropy.errors import messages
from memorization.models import Connections


@pytest.mark.django_db
class TestConnectionsModelPositive:
    """
    Positive tests on 'Connections' model.
    """
    def test_create_model_instance(self, one_word):
        """
        Check that model instance can be successfully created provided that correct set
        of data has been supplied.
        """
        english = one_word('english', save_to_db=True)
        russian = one_word('russian', save_to_db=True)

        Connections.objects.create(
            from_word=english,
            to_word=russian,
        )

        assert Connections.objects.filter(from_word=english, to_word=russian).exists()


@pytest.mark.django_db
class TestConnectionsModelNegative:
    """
    Negative tests on 'Connections' model.
    """
    def test_clean(self, one_word):
        """
        Check that one word can't point on itself.
        """
        english = one_word('english', save_to_db=True)
        expected_error_message = str(messages.memo_connections_1)

        with pytest.raises(exceptions.ValidationError, match=expected_error_message):
            Connections.objects.create(from_word=english, to_word=english)

    def test_word_ne_self_check_constraint(self, one_word):
        """
        Check if instance point on itself on db level, than IntegrityError is arisen.
        """
        english = one_word('english', save_to_db=True)
        expected_error_message = 'word_ne_self_check'

        with pytest.raises(IntegrityError, match=expected_error_message):
            instance = Connections(from_word=english, to_word=english)
            instance.save(fc=False)
