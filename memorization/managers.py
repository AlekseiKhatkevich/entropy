from typing import Container, Optional

from django.db import models
from django.db.models import Q
from django.db.models.expressions import RawSQL


class WordManager(models.Manager):
    """
    Manager for 'Word' model.
    """
    def word_translations(self,
                          pk: int,
                          languages: Optional[Container[str]] = None,
                          ) -> Container[models.Model]:
        """
        Method returns list of word's translations in all languages by default.
        pk - primary key of the word.
        languages - iterable of languages to restrict return with.
        """
        table = self.model.translation.through._meta.db_table
        # noinspection SqlResolve
        pks_of_linked_words = \
            f"""
            WITH RECURSIVE translations AS (
            SELECT
                    from_word_id,
                    to_word_id
            FROM
                    {table}
            WHERE
                    from_word_id={pk} OR to_word_id={pk}
            UNION
                SELECT
                    recurcive.from_word_id,
                    recurcive.to_word_id
                FROM
                     {table} AS recurcive
                INNER JOIN
                    translations AS main
                    ON recurcive.to_word_id = main.from_word_id
        )
            (
            SELECT
                from_word_id
            FROM
                translations
            UNION
            SELECT
                to_word_id
            FROM
                translations
            EXCEPT SELECT {pk}
            )
    """
        pks_of_linked_words = RawSQL(pks_of_linked_words, ())
        matches = self.model.objects.filter(
            Q(first_word__from_word_id__in=pks_of_linked_words) |
            Q(first_word__to_word_id__in=pks_of_linked_words)
        ).exclude(pk=pk).distinct()

        if languages is not None:
            matches = matches.filter(language_id__in=languages)

        return matches

