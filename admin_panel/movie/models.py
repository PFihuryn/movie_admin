import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FilmWorkType(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    TV_SHOW = 'tv_show', _('TV_show')


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('Actor')
    DIRECTOR = 'director', _('Director')
    WRITER = 'writer', _('Writer')


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        managed = False

    def __str__(self):
        return self.name


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    creation_date = models.DateField(_('Creation date'), null=True, blank=True)
    rating = models.FloatField(
        _('Rating'),
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )
    type = models.CharField(
        _('Type'),
        max_length=20,
        choices=FilmWorkType.choices,
        default=FilmWorkType.MOVIE,
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreFilmWork',
        verbose_name=_('Genres'),
    )
    persons = models.ManyToManyField(
        'Person',
        through='PersonFilmWork',
        verbose_name=_('Persons'),
    )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('FilmWork')
        verbose_name_plural = _('FilmWorks')
        managed = False

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin,):
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        to_field='id',
        db_column='genre_id',
    )
    film_work = models.ForeignKey(
        'FilmWork',
        on_delete=models.CASCADE,
        to_field='id',
        db_column='film_work_id',
    )
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=['film_work_id', 'genre_id'],
                name='genre_film_work',
            ),
        ]
        verbose_name = _('GenreFilmWork')
        verbose_name_plural = _('GenreFilmWorks')
        managed = False


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('FullName'), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        managed = False

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, to_field='id', db_column='person_id')
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE, to_field='id', db_column='film_work_id')
    role = models.CharField(_('Role'), max_length=50, choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('PersonFilmWork')
        verbose_name_plural = _('PersonFilmWorks')
        constraints = [
            models.UniqueConstraint(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_role'),
        ]
        managed = False
