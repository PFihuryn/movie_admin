from django.contrib import admin, messages
from django.contrib.admin.options import csrf_protect_m
from django.db import OperationalError
from django.shortcuts import redirect
from django.utils.connection import ConnectionDoesNotExist
from django_summernote.admin import SummernoteModelAdmin

from notification.exceptions import SendingToSchedulerExceptions
from notification.models import (
    EventNotification,
    Mail,
    NewFilm,
    Notification,
    Schedule,
    Subscribe,
    NotificationTemplate,
)
from utils.use_db_admin_mixin import UseDbAdminMixin


class NotificationModelAdmin(UseDbAdminMixin):
    """Определяем БД для работы."""

    using = 'notification_db'


@admin.register(Notification,)
class NotificationAdmin(NotificationModelAdmin):
    """ Админка для рассылок."""

    list_display = 'name', 'destination'


@admin.register(Schedule)
class ScheduleAdmin(NotificationModelAdmin):
    """ Админка для расписания рассылок."""

    list_display = 'notification',
    list_select_related = True

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except SendingToSchedulerExceptions as exc:
            self.message_user(request, exc.args[0], level=messages.ERROR)


@admin.register(NotificationTemplate)
class TemplateAdmin(SummernoteModelAdmin, NotificationModelAdmin):
    """Админка для шаблонов сообщений."""

    summernote_fields = 'template',
    list_display = 'name', 'subject', 'notification'
    list_select_related = True


@admin.register(Subscribe)
class SubscribeAdmin(NotificationModelAdmin):
    """Админка для подписок пользователя."""

    list_display = 'user_id', 'notification'
    list_select_related = True


@admin.register(Mail)
class MailAdmin(NotificationModelAdmin):
    """Админка для сообщений для пользователя."""

    list_display = 'email',
    readonly_fields = 'context', 'email', 'created'


@admin.register(EventNotification)
class EventNotificationAdmin(NotificationModelAdmin):
    """Админка для сопоставления событий и рассылок."""

    list_display = 'event', 'notification'
    list_select_related = True


@admin.register(NewFilm)
class NewFilmAdmin(NotificationModelAdmin):
    """Админка для новинок фильмов."""

    list_display = 'film', 'genre', 'date'
