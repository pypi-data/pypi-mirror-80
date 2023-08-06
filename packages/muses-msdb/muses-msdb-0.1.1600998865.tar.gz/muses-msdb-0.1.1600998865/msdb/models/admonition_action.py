from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel, Admonition


class AdmonitionActionManager(models.Manager):
    pass


class AdmonitionAction(BaseModel):
    SYSTEM_ACTION = 'systemAction'
    MESSAGE_TO_USER = 'msgToUser'
    MESSAGE_FROM_USER = 'msgFromUser'
    INTERNAL_MESSAGE = 'internalMsg'
    TYPE_CHOICES = (
        (SYSTEM_ACTION, _('System Action')),
        (MESSAGE_FROM_USER, _('Message from member')),
        (MESSAGE_TO_USER, _('Message to member')),
        (INTERNAL_MESSAGE, _('Internal message'))
    )
    message = models.TextField(
        verbose_name=_('message'),
    )
    type = models.CharField(
        verbose_name=_('type'),
        max_length=30,
        choices=TYPE_CHOICES,
        default=SYSTEM_ACTION
    )
    admonition = models.ForeignKey(
        to=Admonition,
        on_delete=models.CASCADE
    )
    objects = AdmonitionActionManager()
