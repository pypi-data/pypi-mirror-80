from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel, License


class BookManager(models.Manager):
    pass


class Book(BaseModel):
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255
    )
    isbn = models.CharField(
        verbose_name=_('isbn'),
        max_length=20,
    )
    published_at = models.DateField(
        verbose_name=_('published date')
    )
    author = models.ForeignKey(
        to=Member,
        related_name='book_author',
        on_delete=models.CASCADE
    )
    license = models.ForeignKey(
        to=License,
        related_name='book_license',
        on_delete=models.CASCADE,
    )
    visible = models.BooleanField(
        verbose_name=_('visible'),
        unique=False,
        null=False,
        blank=False,
        default=False
    )

    def __str__(self):
        return self.title

    objects = BookManager()

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'
