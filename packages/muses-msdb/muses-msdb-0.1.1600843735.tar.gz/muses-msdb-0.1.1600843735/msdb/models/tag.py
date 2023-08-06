from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel, Section


class TagManager(models.Manager):
    pass


class Tag(BaseModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        db_index=True
    )
    enable_at = models.DateTimeField(
        verbose_name=_('enable at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True
    )
    disable_at = models.DateTimeField(
        verbose_name=_('disable at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True
    )
    CATEGORY = 0
    THEME = 1
    PROSODY = 2
    FORM = 3
    USER = 4
    EVENT = 5
    TYPE_CHOICES = (
        (CATEGORY, _('category')),
        (THEME, _('theme')),
        (PROSODY, _('prosody')),
        (FORM, _('form')),
        (USER, _('user')),
        (EVENT, _('event')),
    )
    type = models.CharField(
        verbose_name=_('type'),
        unique=False,
        null=False,
        blank=True,
        db_index=False,
        max_length=255,
        choices=TYPE_CHOICES,
        default=USER
    )
    mature = models.BooleanField(
        verbose_name=_('mature'),
        unique=False,
        null=False,
        blank=True,
        default=False
    )
    active = models.BooleanField(
        verbose_name=_('active'),
        unique=False,
        null=False,
        blank=False,
        default=False
    )

    valid_sections = models.ManyToManyField(
        to=Section
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
