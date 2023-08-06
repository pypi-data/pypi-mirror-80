from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Member, BaseModel, Post, Comment


class Rating(models.Model):
    level = models.PositiveSmallIntegerField(
        verbose_name=_('level'),
        unique=False,
        null=False,
        blank=False,
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
    )
    owner = models.ForeignKey(
        verbose_name=_('owner'),
        to=Member,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        abstract = True


class PostRatingManager(models.Manager):
    pass


class PostRating(BaseModel, Rating):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE
    )
    objects = PostRatingManager()


class CommentRatingManager(models.Manager):
    pass


class CommentRating(BaseModel, Rating):
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE
    )
    objects = CommentRatingManager()


