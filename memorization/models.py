from django.contrib.auth import get_user_model
from django.core import exceptions
from django.db import models
from django.db.models import F, Q
from django.utils import timezone

from entropy.errors import messages
from memorization import language_codes, managers


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
        to_field='code',
    )
    second_language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        verbose_name='second language',
        related_name='second_language',
        to_field='code',
    )

    class Meta:
        verbose_name = 'Language family'
        verbose_name_plural = 'Language families'
        unique_together = ('first_language', 'second_language', 'name',)
        index_together = ('first_language', 'second_language',)
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
    Represents language. This table populated via custom migration, and it is read-only.
    """
    code = models.CharField(
        verbose_name='country code acc. ISO 639',
        max_length=2,
        editable=False,
        primary_key=True,
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
                )),)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.pk=} ~ {self.code=}'

    def save(self, fc=True, *args, **kwargs):
        if fc:
            self.full_clean()
        super().save(*args, **kwargs)


class Connections(models.Model):
    """
    Model represents connections between words in different languages.
    """
    from_word = models.ForeignKey(
        'Word',
        on_delete=models.CASCADE,
        verbose_name='first word',
        related_name='first_word',
    )
    to_word = models.ForeignKey(
        'Word',
        on_delete=models.CASCADE,
        verbose_name='second word',
        related_name='second_word',
    )

    class Meta:
        verbose_name = 'Word connection'
        verbose_name_plural = 'Word connections'
        unique_together = ('to_word', 'from_word',)
        constraints = (
            # first word can't be equal to second word.
            models.CheckConstraint(
                name='word_ne_self_check',
                check=~Q(from_word=F('to_word')),
            ),)

    def __str__(self):
        return f'{self.from_word.name} / {self.to_word.name}'

    def __repr__(self):
        return f'{self.from_word=} / {self.to_word=}'

    def clean(self):
        if self.from_word == self.to_word:
            raise exceptions.ValidationError(
                *messages.memo_connections_1,
            )

    def save(self, fc=True, *args, **kwargs):
        if fc:
            self.full_clean()
        super().save(*args, **kwargs)


class Word(models.Model):
    """
    Represents one word and relationship between this word and other possible words.
    """
    objects = managers.WordManager()

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
        to_field='code',
    )
    translation = models.ManyToManyField(
        'self',
        verbose_name='same words in another languages',
        related_name='translations',
        symmetrical=True,
        related_query_name='word',
        through=Connections,
        through_fields=('from_word', 'to_word',),
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
        default=timezone.now,
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
        constraints = (
            models.CheckConstraint(
                name='entry_date_vs_memorization_date_check',
                check=Q(entry_date__lte=F('memorization_date')),
            ),)

    def __str__(self):
        return f'{self.word.name} in {self.learn_in_language.name}'

    def __repr__(self):
        return f'{self.id=} ~ {self.word.name=} ~ {self.learn_in_language.name=}'

    def clean(self):
        errors = {}
        # Cant' lear word in same language. makes no sense.
        if self.learn_in_language == self.word.language:
            errors |= {
                'learn_in_language': exceptions.ValidationError(
                    *messages.memo_notebook_1,
                )}
        # Entry date should be earlier than memorization date.
        if None not in (self.entry_date, self.memorization_date) \
                and (self.entry_date >= self.memorization_date):
            errors |= {
                'memorization_date': exceptions.ValidationError(
                    *messages.memo_notebook_2,
                )}

        if errors:
            raise exceptions.ValidationError(errors)

    def save(self, fc=True, *args, **kwargs):
        if fc:
            self.full_clean()
        super().save(*args, **kwargs)
