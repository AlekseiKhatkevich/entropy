from django.db import models
from memorization import language_codes


class Family:
    """
    Represents language group of family (Latin, Scandinavian, etc)
    """
    name = models.CharField(
        verbose_name='language family',
        unique=True,
        max_length=25,
    )
    first_language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        verbose_name='first language',
    )
    second_language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        verbose_name='second language',
    )

    class Meta:
        verbose_name = 'Language family'
        verbose_name_plural = 'Language families'
        unique_together = ('first_language', 'second_language', 'name',)


class Language(models.Model):
    """
    Represents language.
    """
    code = models.CharField(
        verbose_name='country code acc. ISO 639',
        max_length=2,
        editable=False,
    )
    name = models.CharField(
        verbose_name='language name',
        max_length=23,
        editable=False,
    )
    family = models.ManyToManyField(
        'self',
        verbose_name='language family',
        null=True,
        blank=True,
        related_name='family',
        related_query_name='language',
        symmetrical=True,
        through=Family,
        through_fields=('first_language', 'second_language'),
    )

    def __str__(self):
        return self.name

    class Meta:
        # check_contrsint
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'


# class Word(models.Model):
#     """
#     Represents one word and relationship between this word and other possible words.
#     """
#     word = models.CharField(
#         max_length=30,
#         verbose_name='one word name',
#         unique=True,
#     )
#     definition = models.CharField(
#         max_length=300,
#         verbose_name='one word definition',
#     )
#     language = models.CharField(
#
#     )
#
#     def __str__(self):
#         pass
#
#     class Meta:
#         pass
