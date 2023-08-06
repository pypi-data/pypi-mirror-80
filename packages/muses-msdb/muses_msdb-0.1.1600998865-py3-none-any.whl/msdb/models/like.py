from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import BaseModel, Member, Post, Comment


class Like(models.Model):
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


class PostLikeManager(models.Manager):
    pass


class PostLike(BaseModel, Like):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE
    )
    objects = PostLikeManager()


class CommentLikeManager(models.Manager):
    pass


class CommentLike(BaseModel, Like):
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE
    )
    objects = CommentLikeManager()
