from django.db import models
from typing import Optional, Type, TypeVar

from django.db.models import *

class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super().db_type(connection)


class PositiveTinyIntegerField(models.SmallIntegerField, models.fields.PositiveIntegerRelDbTypeMixin):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint unsigned"
        else:
            return super().db_type(connection)

T = TypeVar('T', bound='models.Model')

def make_fk(model_kclass: Type[T], column_name: str, related_name: Optional[str] = None, null: bool = False) -> T:
    return models.ForeignKey(
        model_kclass, # type: ignore
        db_column=column_name,
        related_name="+" if related_name is None else related_name,
        on_delete=models.CASCADE,
        null=null, # type: ignore
        blank=null
    )