from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from utils.use_db_admin_mixin import UseDbAdminMixin
from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


class MovieModelAdmin(UseDbAdminMixin):
    """Определяем БД для работы."""

    using = 'movie_db'


@admin.register(Genre)
class GenreAdmin(MovieModelAdmin):
    list_display = 'name', 'description',
    search_fields = 'name',
    empty_value_display = _('-empty-')
    ordering = 'name',


class GenreInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 0
    verbose_name = _('Genre')
    autocomplete_fields = 'genre',

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('genre', 'film_work')


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 0
    verbose_name = _('PersonFilmWork')
    autocomplete_fields = 'person',

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('person', 'film_work')


@admin.register(FilmWork)
class FilmworkAdmin(MovieModelAdmin):
    list_display = 'title', 'type', 'creation_date', 'rating'
    list_filter = 'type',
    search_fields = 'title', 'description', 'id'
    empty_value_display = _('-empty-')
    inlines = [GenreInline, PersonFilmWorkInline]
    ordering = 'title',


@admin.register(Person)
class PersonAdmin(MovieModelAdmin):
    list_display = 'full_name',
    search_fields = 'full_name', 'id'
    empty_value_display = _('-empty-')
    ordering = 'full_name',
