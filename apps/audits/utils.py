import copy
from datetime import datetime
from itertools import chain

from django.db import models

from common.db.fields import RelatedManager
from common.utils import validate_ip, get_ip_city, get_logger
from common.utils.timezone import as_current_tz
from .const import DEFAULT_CITY

logger = get_logger(__name__)


def write_login_log(*args, **kwargs):
    from audits.models import UserLoginLog

    ip = kwargs.get('ip') or ''
    if not (ip and validate_ip(ip)):
        ip = ip[:15]
        city = DEFAULT_CITY
    else:
        city = get_ip_city(ip) or DEFAULT_CITY
    kwargs.update({'ip': ip, 'city': city})
    return UserLoginLog.objects.create(**kwargs)


def _get_instance_field_value(
        instance, include_model_fields,
        model_need_continue_fields, exclude_fields=None
):
    data = {}
    opts = getattr(instance, '_meta', None)
    if opts is not None:
        for f in chain(opts.concrete_fields, opts.private_fields):
            if not include_model_fields and not getattr(f, 'primary_key', False):
                continue

            if isinstance(f, (models.FileField, models.ImageField)):
                continue

            if getattr(f, 'attname', None) in model_need_continue_fields:
                continue

            value = getattr(instance, f.name, None) or getattr(instance, f.attname, None)
            if not isinstance(value, bool) and not value:
                continue

            if getattr(f, 'primary_key', False):
                f.verbose_name = 'id'
            elif isinstance(value, list):
                value = copy.deepcopy(value)
            elif isinstance(value, dict):
                value = dict(copy.deepcopy(value))
            elif isinstance(value, datetime):
                value = as_current_tz(value).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, RelatedManager):
                value = value.value
            elif isinstance(f, models.OneToOneField) and isinstance(value, models.Model):
                nested_data = _get_instance_field_value(
                    value, include_model_fields, model_need_continue_fields, ('id',)
                )
                for k, v in nested_data.items():
                    if exclude_fields and k in exclude_fields:
                        continue
                    data.setdefault(k, v)
                continue
            data.setdefault(str(f.verbose_name), value)
    return data


def model_to_dict_for_operate_log(
        instance, include_model_fields=True, include_related_fields=False
):
    model_need_continue_fields = ['date_updated']
    m2m_need_continue_fields = ['history_passwords']

    data = _get_instance_field_value(
        instance, include_model_fields, model_need_continue_fields
    )

    if include_related_fields:
        opts = instance._meta
        for f in opts.many_to_many:
            value = []
            if instance.pk is not None:
                related_name = getattr(f, 'attname', '') or getattr(f, 'related_name', '')
                if not related_name or related_name in m2m_need_continue_fields:
                    continue
                try:
                    value = [str(i) for i in getattr(instance, related_name).all()]
                except:
                    pass
            if not value:
                continue
            try:
                field_key = getattr(f, 'verbose_name', None) or f.related_model._meta.verbose_name
                data.setdefault(str(field_key), value)
            except:
                pass
    return data
