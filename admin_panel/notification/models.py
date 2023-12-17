import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from notification.web_services.scheduler import send_notification


class UUIDMixin(models.Model):
    """Добавляем uuid к таблице."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    """Добавляем временную метку к таблице."""

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Freq(models.TextChoices):
    """Частота вызова задач по расписанию."""

    YEARLY = _('Yearly')
    MONTHLY = _('Monthly')
    WEEKLY = _('Weekly')
    DAILY = _('Daily')
    HOURLY = _('Hourly')
    MINUTELY = _('Minutely')
    SECONDLY = _('Secondly')


class NotificationType(models.TextChoices):
    """Частота вызова задач по расписанию."""

    EMAIL = _('Email')
    PUSH = _('PUSH')
    SMS = _('SMS')


class Notification(UUIDMixin):
    """Рассылка уведомлений."""

    name = models.CharField(_('Name'), max_length=255, unique=True)
    description = models.TextField(_('Description'), blank=True)
    destination = models.CharField(
        _('Destination'),
        max_length=64,
        choices=NotificationType.choices,
    )

    class Meta:
        db_table = 'notifications"."notification'
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return f'{self.name} - {self.destination}'


class Schedule(UUIDMixin):
    """Расписание рассылки."""

    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    freq = models.CharField(
        max_length=16,
        choices=Freq.choices,
        null=True,
        blank=True,
    )
    dtstart = models.DateTimeField(
        help_text=_(
            'The recurrence start. Besides being the base for the recurrence, '
            'missing parameters in the final recurrence instances will also '
            'be extracted from this date. If not given, datetime.now() will '
            'be used instead'
        ),
        null=True,
        blank=True,
    )
    interval = models.PositiveSmallIntegerField(
        help_text=_(
            'The interval between each freq iteration. For example, when '
            'using YEARLY, an interval of 2 means once every two years, but '
            'with HOURLY, it means once every two hours. The default '
            'interval is 1'
        ),
        null=True,
        blank=True,
    )
    wkst = models.CharField(
        max_length=255,
        help_text=_(
            'The week start day. Must be one of the MO, TU, WE constants, or '
            'an integer, specifying the first day of the week. This will '
            'affect recurrences based on weekly periods. The default week '
            'start is got from calendar.firstweekday(), and may be modified '
            'by calendar.setfirstweekday()'
        ),
        blank=True,
    )
    count = models.PositiveSmallIntegerField(
        help_text=_(
            'If given, this determines how many occurrences will be generated'
        ),
        null=True,
        blank=True,
    )
    until = models.DateTimeField(
        help_text=_(
            'If given, this must be a datetime instance specifying the '
            'upper-bound limit of the recurrence. The last recurrence in the '
            'rule is the greatest datetime that is less than or equal to the '
            'value specified in the until parameter'
        ),
        null=True,
        blank=True,
    )
    bysetpos = ArrayField(
        models.PositiveSmallIntegerField(null=True, blank=True),
        help_text=_(
            'If given, it must be either an integer, or a sequence of '
            'integers, positive or negative. Each given integer will specify '
            'an occurrence number, corresponding to the nth occurrence of the '
            'rule inside the frequency period. For example, a bysetpos of -1 '
            'if combined with a MONTHLY frequency, and a byweekday of (MO, '
            'TU, WE, TH, FR), will result in the last work day of every month.'
        ),
        null=True,
        blank=True,
    )
    bymonth = ArrayField(
        models.PositiveSmallIntegerField(null=True, blank=True),
        help_text=_(
            'If given, it must be either an integer, or a sequence of '
            'integers, meaning the months to apply the recurrence to'
        ),
        null=True,
        blank=True,
    )
    bymonthday = ArrayField(
        models.PositiveSmallIntegerField(null=True, blank=True),
        help_text=_(
            'If given, it must be either an integer, or a sequence of '
            'integers, meaning the month days to apply the recurrence to'
        ),
        null=True,
        blank=True,
    )
    byyearday = ArrayField(
        models.PositiveSmallIntegerField(null=True, blank=True),
        help_text=_(
            'If given, it must be either an integer, or a sequence of '
            'integers, meaning the year days to apply the recurrence to'
        ),
        null=True,
        blank=True,
    )
    byeaster = ArrayField(
        models.SmallIntegerField(null=True, blank=True),
        help_text=_(
            'If given, it must be either an integer, or a sequence of '
            'integers, positive or negative. Each integer will define an '
            'offset from the Easter Sunday. Passing the offset 0 to byeaster '
            'will yield the Easter Sunday itself. This is an extension to '
            'the RFC specification'
        ),
        null=True,
        blank=True,
    )
    byweekno = ArrayField(
        models.SmallIntegerField(null=True, blank=True),
        help_text=_(
            'If given, it must be either an integer, or a sequence of '
            'integers, meaning the week numbers to apply the recurrence to. '
            'Week numbers have the meaning described in ISO8601, that is, '
            'the first week of the year is that containing at least four '
            'days of the new year'
        ),
        null=True,
        blank=True,
    )
    byhour = ArrayField(
        models.PositiveSmallIntegerField(null=True, blank=True),
        help_text=_(
            'If given, it must be either an integer, or a sequence of '
            'integers, meaning the hours to apply the recurrence to.'
        ),
        null=True,
        blank=True,
    )
    byminute = ArrayField(
        models.PositiveSmallIntegerField(null=True, blank=True),
        help_text=_(
            'If given, it must be either an integer, or a sequence of '
            'integers, meaning the minutes to apply the recurrence to.'
        ),
        null=True,
        blank=True,
    )
    bysecond = ArrayField(
        models.PositiveSmallIntegerField(null=True, blank=True),
        help_text=_(
            'If given, it must be either an integer, or a sequence of '
            'integers, meaning the seconds to apply the recurrence to.'
        ),
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'notifications"."schedule'
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedule')

    def __str__(self):
        return self.notification.name

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None,
    ):
        super().save(force_insert, force_update, using, update_fields)
        # Отправляем данные планировщику
        send_notification(self)


class Subscribe(UUIDMixin):
    """Подписки пользователей.

    Если пользователь не задан, это означает рассылку на всех
    зарегистрированных пользователей.
    """

    user_id = models.UUIDField(_('User'), null=True, blank=True)
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."subscribe'
        verbose_name = _('Subscribe')
        verbose_name_plural = _('Subscribes')


class NotificationTemplate(UUIDMixin):
    """Шаблон для рассылки."""

    name = models.CharField(_('Name'), max_length=255)
    subject = models.CharField(_('Subject'), max_length=255)
    template = models.TextField(
        _("HTML code or Text"), null=False,
        blank=False, default='',
    )
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."template'
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def __str__(self):
        return self.name


class Mail(UUIDMixin, TimeStampedMixin):
    """Сообщение для пользователя."""

    context = models.TextField(blank=False, null=False)
    email = models.EmailField(_('Email'))

    class Meta:
        db_table = 'notifications"."mail'
        verbose_name = _('Mail')
        verbose_name_plural = _('Mails')

    def __str__(self):
        return f'{self.email} - {self.created}'


class EventNotification(UUIDMixin):
    """Таблица-связка событий сторонних сервисов и рассылок."""

    event = models.CharField(_('Event'), max_length=255)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."event_notification'
        verbose_name = _('Event Notification')
        verbose_name_plural = _('Events Notifications')


class NewFilm(UUIDMixin, TimeStampedMixin):
    """Новинки фильмов."""

    film = models.UUIDField(_('Film'))
    genre = models.UUIDField(_('Genre'))
    date = models.DateTimeField(_('Date'))

    class Meta:
        db_table = 'notifications"."new_film'
        verbose_name = _('New film')
        verbose_name_plural = _('New films')
        indexes = [
            models.Index(fields=['date', ], name='new_film_date'),
        ]
