from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models.base import TimeStampedMixin, UUIDMixin
from authentication.models.users import User


class UsersHistory(UUIDMixin, TimeStampedMixin):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    source = models.CharField(_('Source'), max_length=128)
    login_time = models.DateTimeField(_('Login time'), auto_now=True)

    class Meta:
        db_table = 'auth"."users_history'
        verbose_name = _('User history')
        verbose_name_plural = _('Users history')
        managed = False

    def __str__(self):
        return f'<Login user {self.user_id}>'


class ThirdPartyUser(UUIDMixin):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    third_party_id = models.CharField(
        _('Third party id'),
        max_length=128,
    )
    third_party_title = models.CharField(
        _('Third party title'),
        max_length=50,
    )

    class Meta:
        db_table = 'auth"."third_party_user'
        verbose_name = _('Third party user')
        verbose_name_plural = _('Third party users')
        managed = False

    def __str__(self):
        return f'<Login user {self.user_id}>'
