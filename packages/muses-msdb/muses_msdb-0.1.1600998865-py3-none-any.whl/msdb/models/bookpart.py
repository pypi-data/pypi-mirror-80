from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel, Book


class BookPartManager(models.Manager):
    pass


class BookPart(BaseModel):
    title = models.CharField(
        verbose_name=_('title'),
        unique=False,
        null=False,
        blank=False,
        db_index=True,
        max_length=255
    )
    order = models.IntegerField(
        verbose_name=_('order'),
        unique=False,
        null=True,
        blank=True,
        db_index=False
    )
    book = models.ForeignKey(
        to=Book,
        related_name='book_ref',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    objects = BookPartManager()

    class Meta:
        verbose_name = 'bookpart'
        verbose_name_plural = 'bookparts'
