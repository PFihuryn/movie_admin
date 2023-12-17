from django.utils.translation import gettext_lazy as _
from djongo import models


class Bookmark(models.Model):
    _id = models.ObjectIdField()

    user_id = models.CharField(_('User id'), max_length=60)
    movie_id = models.CharField(_('Movie id'), max_length=60)

    class Meta:
        db_table = 'bookmarks'

    def __str__(self):
        return f'{self.user_id} - {self.movie_id}'


class TargetType(models.TextChoices):
    movie = 'movie'
    review = 'review'


class Like(models.Model):
    _id = models.ObjectIdField()

    user_id = models.CharField(_('User id'), max_length=60)
    target_id = models.CharField(_('Target id'), max_length=60)
    target_type = models.CharField(
        _('Target type'),
        max_length=60,
        choices=TargetType.choices,
        default=TargetType.movie.value,
    )

    class Meta:
        db_table = 'likes'

    def __str__(self):
        return f'{self.user_id} - {self.target_id}'


class Review(models.Model):
    _id = models.ObjectIdField()

    user_id = models.CharField(_('User id'), max_length=60)
    movie_id = models.CharField(_('Movie id'), max_length=60)
    review = models.TextField(_('Review'), blank=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f'{self.user_id} - {self.movie_id}'


class User(models.Model):
    _id = models.ObjectIdField()

    username = models.CharField(_('User name'), max_length=60)
    email = models.EmailField(_('Email'), )
    full_name = models.CharField(
        _('Full name'),
        max_length=128,
        blank=True,
    )

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class WatchProgress(models.Model):
    _id = models.ObjectIdField()

    user_id = models.CharField(_('User id'), max_length=60)
    movie_id = models.EmailField(_('Movie id'), max_length=60)
    progress = models.FloatField(_('Progress'), )

    class Meta:
        db_table = 'watch_progress'

    def __str__(self):
        return f'{self.user_id} - {self.movie_id}'
