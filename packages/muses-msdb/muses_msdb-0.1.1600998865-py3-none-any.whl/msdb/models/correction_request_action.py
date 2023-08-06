from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BaseModel, Member, CorrectionRequest


class CorrectionRequestActionManager(models.Manager):
    pass


class CorrectionRequestAction(BaseModel):
    CORRECTION = 1
    VALIDATION = 2
    ACTION_CHOICES = (
        (CORRECTION, _('Correction')),
        (VALIDATION, _('Validation'))
    )
    owner = models.ForeignKey(
        to=Member,
        on_delete=models.DO_NOTHING
    )
    correction_request = models.ForeignKey(
        to=CorrectionRequest,
        on_delete=models.DO_NOTHING
    )
    action = models.CharField(
        verbose_name=_('action'),
        max_length=30,
        choices=ACTION_CHOICES,
        default=CORRECTION
    )

    objects = CorrectionRequestActionManager()

    class Meta:
        verbose_name = 'Correction Request'
        verbose_name_plural = 'Correction Requests'
