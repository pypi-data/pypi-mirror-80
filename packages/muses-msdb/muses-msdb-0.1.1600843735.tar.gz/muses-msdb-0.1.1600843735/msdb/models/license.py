from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel


class LicenseManager(models.Manager):
    pass


class License(BaseModel):
    name: str = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        null=True
    )
    text = models.TextField(
        verbose_name=_('text'),
        null=True
    )
    logo = models.ImageField(
        verbose_name=_('logo'),
        null=True
    )
    active = models.BooleanField(
        verbose_name=_('active'),
        unique=False,
        null=False,
        blank=False,
        default=False
    )

    def __str__(self):
        return self.name

    objects = LicenseManager()

    class Meta:
        verbose_name = 'license'
        verbose_name_plural = 'licenses'
