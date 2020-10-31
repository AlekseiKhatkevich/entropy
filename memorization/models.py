from django.db import models
from django.db.models import Q

from memorization import language_codes


class Family(models.Model):
    """
    Represents language group of family (Latin, Scandinavian, etc)
    """
    name = models.CharField(
        verbose_name='language family',
        max_length=25,
    )
    first_language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        verbose_name='first language',
        related_name='first_language',
    )
    second_language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        verbose_name='second language',
        related_name='second_language',
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.id=} ~ {self.name=} ~ {self.first_language.name=} ~ {self.second_language.name=}'

    class Meta:
        verbose_name = 'Language family'
        verbose_name_plural = 'Language families'
        unique_together = ('first_language', 'second_language', 'name',)
        index_together = ('first_language', 'second_language', )


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
        max_length=28,
        editable=False,
    )
    family = models.ManyToManyField(
        'self',
        verbose_name='language family',
        related_name='family',
        related_query_name='language',
        symmetrical=True,
        through=Family,
        through_fields=('first_language', 'second_language'),
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.id=} ~ {self.code=}'

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        unique_together = ('code', 'name',)
        constraints = (
            models.CheckConstraint(
                name='language_code_check',
                check=Q(
                    code__in=language_codes.language_codes,
                )), )


class Word(models.Model):
    """
    Represents one word and relationship between this word and other possible words.
    """
    word = models.CharField(
        max_length=30,
        verbose_name='one word',
        db_index=True,
    )
    definition = models.CharField(
        max_length=300,
        verbose_name='one word definition',
    )
    language = models.ForeignKey(
        Language,
        verbose_name='language of the word',
        on_delete=models.PROTECT,
    )
    translation = models.ManyToManyField(
        'self',
        verbose_name='same words in another languages',
        related_name='translation',
        symmetrical=True,
    )

    def __str__(self):
        return f'{self.word} in {self.language.name}'

    def __repr__(self):
        return f'{self.id=} ~ {self.word=} ~ {self.language.name=}'

    class Meta:
        verbose_name = 'Word'
        verbose_name_plural = 'Words'
        unique_together = ('word', 'language',)
