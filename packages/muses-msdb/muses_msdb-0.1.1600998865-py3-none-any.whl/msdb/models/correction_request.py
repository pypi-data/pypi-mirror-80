from django.db import models
from django.utils.translation import gettext_lazy as _
from precise_bbcode.fields import BBCodeTextField

from django_editorjs.fields import EditorJSField

from . import BaseModel, Post


class CorrectionRequestManager(models.Manager):
    pass


class CorrectionRequest(BaseModel):
    title = models.CharField(
        verbose_name=_('title'),
        unique=False,
        null=False,
        blank=False,
        max_length=255,
    )
    summary = EditorJSField(
        verbose_name=_('summary'),
        unique=False,
        null=True,
        blank=True,
        max_length=2000,
    )
    bbcode_content = BBCodeTextField(
        verbose_name=_('bbcode content'),
        unique=False,
        null=True,
        blank=True,
    )
    content = EditorJSField(
        verbose_name=_('content'),
        unique=False,
        null=True,
        blank=True,
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.DO_NOTHING
    )
    objects = CorrectionRequestManager()
