from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel
from ..validators import not_passed


class ContestManager(models.Manager):
    pass


class Contest(BaseModel):
    name = models.CharField(
        verbose_name=_('name'),
        unique=False,
        null=False,
        blank=False,
        max_length=255,
        db_index=True
    )
    starts_at = models.DateField(
        verbose_name=_('start at'),
        unique=False,
        null=False,
        blank=False,
        db_index=True,
        validators=[not_passed]
    )
    ends_at = models.DateField(
        verbose_name=_('ends at'),
        unique=False,
        null=False,
        blank=False,
        db_index=True,
        validators=[not_passed]
    )
    objects = ContestManager()
