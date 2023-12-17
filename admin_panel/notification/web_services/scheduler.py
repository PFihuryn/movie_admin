"""Отправка данных с расписанием рассылки в "Планировщик"."""
import json
import logging
import uuid
from datetime import date, datetime

import environs
import requests
from django.db import models
from django.utils.translation import gettext_lazy as _

from notification.exceptions import SendingToSchedulerExceptions

env = environs.Env()
env.read_env()
logger = logging.getLogger(__name__)


def send_notification(notification: models.Model):
    """Отправка информации по модели."""
    field_values = get_field_values(notification)
    content = json.dumps(field_values)
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = get_url()

    try:
        response = requests.post(url, data=content, headers=headers)
    except Exception as exc:
        logger.warning(
            '%s! Service is not available' % exc.__class__.__name__
        )
        raise SendingToSchedulerExceptions(
            _('Scheduler service is not available'),
        )
    if response.status_code != requests.status_codes.codes.created:
        logger.warning(json.loads(response.content))
        logger.warning(
            'Fail! Response status code %s' % response.status_code
        )
        raise SendingToSchedulerExceptions(
            _('Scheduler service connection error'),
        )
    else:
        logger.info(
            'Success. Response status code %s' % response.status_code
        )


def field_value_check(field, field_value, id_fields):
    """Проверка значения полей"""
    if field.name in id_fields:
        field_value = field_value.id
    if type(field_value) in {datetime, date, uuid.UUID}:
        field_value = str(field_value)
    if not field_value:
        field_value = None
    return field_value


def get_field_values(model: models.Model):
    """Получение значений полей модели."""
    field_values = {}
    id_fields = {'notification'}
    for field in model._meta.get_fields():
        try:
            field_value = getattr(model, field.name)
            field_value = field_value_check(field, field_value, id_fields)
        except AttributeError:
            continue
        field_name = (
            f'{field.name}_id' if field.name in id_fields else field.name)
        field_values[field_name] = field_value
    return field_values


def get_url():
    """Получение url для запроса."""
    schedule_host = env.str('SCHEDULE_HOST')
    schedule_port = env.int('SCHEDULE_PORT')
    return f' http://{schedule_host}:{schedule_port}/api/v1/schedule'
