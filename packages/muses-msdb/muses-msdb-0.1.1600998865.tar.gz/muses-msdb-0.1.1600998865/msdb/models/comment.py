from django.db import models
from django.utils.translation import gettext_lazy as _
from django_editorjs.fields import EditorJSField

from . import BaseModel, Member


class CommentManager(models.Manager):
    pass


class Comment(BaseModel):
    author = models.ForeignKey(
        to=Member,
        related_name='comment_author',
        on_delete=models.CASCADE
    )
    content = EditorJSField(
        verbose_name=_('content')
    )
    reply_to = models.ForeignKey(
        to='self',
        related_name='comment_reply_to',
        on_delete=models.CASCADE
    )
    readings = models.ManyToManyField(
        to=Member
    )
    objects = CommentManager()

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
