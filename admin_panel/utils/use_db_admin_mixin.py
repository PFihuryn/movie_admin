from django.contrib import admin, messages
from django.contrib.admin.options import csrf_protect_m
from django.db import OperationalError
from django.shortcuts import redirect
from django.utils.connection import ConnectionDoesNotExist


class UseDbAdminMixin(admin.ModelAdmin):
    """Миксин, определяющий работу с БД."""

    # Атрибут, определяющий использование БД.
    using = 'default'

    def save_model(self, request, obj, form, change):
        """Объявляем в какую БД происходит сохранение."""
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        """Объявляем из какой БД происходит удаление."""
        obj.delete(using=self.using)

    def get_queryset(self, request):
        """Объявляем из какой БД происходит получение объектов моделей."""
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Объявляем как общаться с другими таблицами по FK."""
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Объявляем как общаться с другими таблицами по M2M."""
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs)

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """Переопределяем для отлавливания ошибок о недоступности БД."""
        try:
            return super().changelist_view(request, extra_context)
        except (ConnectionDoesNotExist, OperationalError):
            self.message_user(
                request,
                message=f'The database "{self.using}" is now unavailable! '
                        f'Try later!',
                level=messages.ERROR,
            )
            return redirect('/admin')
