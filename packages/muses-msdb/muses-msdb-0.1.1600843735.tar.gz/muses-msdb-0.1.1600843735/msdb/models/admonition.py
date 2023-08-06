from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel


class AdmonitionManager(models.Manager):
    pass


class Admonition(BaseModel):
    subject = models.CharField(
        verbose_name=_('subject'),
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        max_length=255,
        default=_("no subject")
    )
    content = models.TextField(
        verbose_name=_('content'),
        unique=False,
        null=True,
        blank=True,
    )
    objects = AdmonitionManager()
