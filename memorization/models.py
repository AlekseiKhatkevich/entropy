from django.db import models
from django.db.models import Q, F
from django.core import exceptions
from memorization import language_codes
from django.contrib.auth import get_user_model
from entropy.errors import messages


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

    class Meta:
        verbose_name = 'Language family'
        verbose_name_plural = 'Language families'
        unique_together = ('first_language', 'second_language', 'name',)
        index_together = ('first_language', 'second_language', )
        constraints = (
            # first_language can't be equal to second_language
            models.CheckConstraint(
                name='point_on_itself_check',
                check=~Q(first_language=F('second_language')),
            ),)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.id=} ~ {self.name=} ~ {self.first_language.name=} ~ {self.second_language.name=}'

    def clean(self):
        # First language can't be equal to itself
        if self.first_language == self.second_language:
            raise exceptions.ValidationError(
                *messages.memo_family_1,
            )

    def save(self, fc=True, *args, **kwargs):
        if fc:
            self.full_clean()
        super().save(*args, **kwargs)

    # todo
    def get_absolute_url(self):
        pass


class Language(models.Model):
    """
    Represents language. This table is populated via custom migration and it is read-only.
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

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.id=} ~ {self.code=}'

    def save(self, fc=True, *args, **kwargs):
        if fc:
            self.full_clean()
        super().save(*args, **kwargs)


class Word(models.Model):
    """
    Represents one word and relationship between this word and other possible words.
    """
    name = models.CharField(
        max_length=30,
        verbose_name='one word',
        db_index=True,
    )
    definition = models.CharField(
        max_length=300,
        verbose_name='one word definition',
        null=True,
        blank=True,
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

    class Meta:
        verbose_name = 'Word'
        verbose_name_plural = 'Words'
        unique_together = ('name', 'language',)

    def __str__(self):
        return f'{self.name} in {self.language.name}'

    def __repr__(self):
        return f'{self.id=} ~ {self.name=} ~ {self.language.name=}'

    def save(self, fc=True, *args, **kwargs):
        if fc:
            self.full_clean()
        super().save(*args, **kwargs)


class NoteBook(models.Model):
    """
    Represents list of words to learn.
    """
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='notebook owner',
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        verbose_name='word to learn',
    )
    learn_in_language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        verbose_name='language to learn in',
    )
    entry_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date and time when entry was created',
        editable=False,
    )
    memorization_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='date when word was memorized',
    )
    attempts = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='quantity of memorization attempts',
    )

    class Meta:
        verbose_name = 'Notebook'
        verbose_name_plural = 'Notebooks'
        unique_together = ('word', 'learn_in_language',)

    def __str__(self):
        return f'{self.word.name} in {self.learn_in_language.name}'

    def __repr__(self):
        return f'{self.id=} ~ {self.word.name=} ~ {self.learn_in_language.name=}'

    def save(self, fc=True, *args, **kwargs):
        if fc:
            self.full_clean()
        super().save(*args, **kwargs)


