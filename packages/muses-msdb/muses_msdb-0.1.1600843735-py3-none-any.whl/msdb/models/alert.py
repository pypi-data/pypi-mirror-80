from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel, Post, Comment


class Alert(models.Model):
    PLAGIARISM = 'plagiarism'
    SPELLING = 'spelling'
    BAD_CATEGORY = 'bad_category'
    HATE = 'hate'
    OTHER = 'other'
    TYPE_ALERT_CHOICES = (
        (PLAGIARISM, _('Plagiarism')),
        (SPELLING, _('Spelling')),
        (BAD_CATEGORY, _('Bad category')),
        (HATE, _('Hate')),
        (OTHER, _('Other'))
    )

    OPEN = 1
    CLOSED = 2
    DISCUSSION = 3
    STATUS_CHOICES = (
        (OPEN, _('open')),
        (CLOSED, _('closed')),
        (DISCUSSION, _('discussion'))
    )

    type = models.CharField(
        verbose_name=_('type'),
        max_length=30,
        choices=TYPE_ALERT_CHOICES,
        default=OTHER
    )
    details = models.TextField(
        verbose_name=_('details'),
        max_length=1000,
        default=""
    )
    status = models.IntegerField(
        verbose_name=_('status'),
        default=1
    )

    class Meta:
        abstract = True


class PostAlertManager(models.Manager):
    pass


class PostAlert(BaseModel, Alert):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE
    )

    objects = PostAlertManager()


class CommentAlertManager(models.Manager):
    pass


class CommentAlert(BaseModel, Alert):
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE
    )

    objects = CommentAlertManager()
