from django.contrib import admin

from utils.use_db_admin_mixin import UseDbAdminMixin
from .models import Bookmark, Like, Review, User, WatchProgress


class UserProfileModelAdmin(UseDbAdminMixin):
    """Определяем БД для работы."""

    using = 'profile_db'


@admin.register(Bookmark)
class BookmarkAdmin(UserProfileModelAdmin):
    """Закладки пользователя."""

    list_display = ('_id', 'user_id', 'movie_id')


@admin.register(Like)
class LikeAdmin(UserProfileModelAdmin):
    """Лайки пользователя."""

    list_display = ('_id', 'user_id', 'target_id', 'target_type')


@admin.register(Review)
class ReviewAdmin(UserProfileModelAdmin):
    """Рецензии пользователя."""

    list_display = ('_id', 'user_id', 'movie_id', 'review')


@admin.register(User)
class UserAdmin(UserProfileModelAdmin):
    """Данные пользователя."""

    list_display = ('_id', 'username', 'email', 'full_name')


@admin.register(WatchProgress)
class WatchProgressAdmin(UserProfileModelAdmin):
    """Прогресс просмотра фильма пользователем."""

    list_display = ('_id', 'user_id', 'movie_id', 'progress')
