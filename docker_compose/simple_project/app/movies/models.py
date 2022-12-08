import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created'),
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Modified'),
    )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    creation_date = models.DateField(verbose_name=_('Creation date'))
    file_path = models.FileField(
        max_length=255,
        verbose_name=_('File path'),
        blank=True,
        null=True,
        upload_to='movies/'
    )
    rating = models.FloatField(
        verbose_name=_('Rating'),
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Type(models.TextChoices):
        MOVIE = 'MOVIE', _('Movie')
        TV_SHOW = 'TV_SHOW', _('TV Show')

    type = models.CharField(
        max_length=7,
        choices=Type.choices,
        verbose_name=_('Type'),
    )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        indexes = [
            models.Index(
                fields=['creation_date'],
                name='film_work_creation_date_idx'
            ),
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork',
        on_delete=models.CASCADE,
        verbose_name=_('Filmwork')
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        verbose_name=_('Genre')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Genre of Filmwork')
        verbose_name_plural = _('Genres of Filmwork')
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'film_work'],
                name='genre_film_work_uniq'
            )
        ]
        indexes = [
            models.Index(
                fields=['genre', 'film_work'],
                name='genre_film_work_idx'
            ),
        ]

    def __str__(self):
        return f'{self.film_work.title} - {self.genre.name}'


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(max_length=255, verbose_name=_('Full name'))

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork',
        on_delete=models.CASCADE,
        verbose_name=_('Filmwork')
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        verbose_name=_('Person')
    )

    class Role(models.TextChoices):
        DIRECTOR = 'DIRECTOR', _('Director')
        ACTOR = 'ACTOR', _('Actor')
        WRITER = 'WRITER', _('Writer')

    role = models.CharField(
        max_length=255,
        verbose_name=_('Role'),
        choices=Role.choices,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Person of Filmwork')
        verbose_name_plural = _('Persons of Filmwork')
        constraints = [
            models.UniqueConstraint(
                fields=['person', 'film_work', 'role'],
                name='person_film_work_role_uniq'
            )
        ]
        indexes = [
            models.Index(
                fields=['person', 'film_work', 'role'],
                name='person_film_work_role_idx'
            ),
        ]

    def __str__(self):
        return self.role
