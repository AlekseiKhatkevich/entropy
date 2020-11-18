from django.db import models


class NoteBookManager(models.Manager):
    """
    Manager for 'NoteBook' model.
    """
    sql = \
        """
            WITH RECURSIVE translations AS (
            SELECT
                    from_word_id,
                    to_word_id
            FROM
                    memorization_word_translation
            WHERE
                    from_word_id=35 OR to_word_id=35
            UNION
                SELECT
                    recurcive.from_word_id,
                    recurcive.to_word_id
                FROM
                     memorization_word_translation AS recurcive
                INNER JOIN
                    translations AS main
                    ON recurcive.to_word_id = main.from_word_id
        )
        SELECT DISTINCT
                unnest(ARRAY[from_word_id] || ARRAY[to_word_id]) AS conn_lng_ids
            FROM
               translations
            EXCEPT
                SELECT unnest(ARRAY[35])
    """
