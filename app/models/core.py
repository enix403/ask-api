from __future__ import annotations
from django.db import models
from typing import TYPE_CHECKING, ClassVar, TypeVar, Generic

T = TypeVar('T', bound='BaseModel')

class BaseModel(models.Model, Generic[T]):
    objects: models.Manager[T]

    class Meta:
        abstract = True
