import uuid

from django.db import models


class UUIDMixin(models.Model):
    """Добавляем uuid к таблице."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    """Добавляем временную метку к таблице."""

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
