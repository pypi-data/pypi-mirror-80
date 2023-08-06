from django.db import models
from django.utils.translation import gettext_lazy as _
from django_editorjs.fields import EditorJSField
from precise_bbcode.fields import BBCodeTextField

from . import BaseModel, Member, Tag, BookPart, Section


class PostManager(models.Manager):
    pass


class Post(BaseModel):
    old_slug = models.URLField(
        verbose_name=_('old slug'),
        max_length=2048,
    )
    DRAFT = 'draft'
    PUBLISHED = 'published'
    WARNED = 'warned'
    ARCHIVED = 'archived'
    POST_STATUS_CHOICES = [
        (DRAFT, _('DRAFT')),
        (PUBLISHED, _('PUBLISHED')),
        (WARNED, _('WARNED')),
        (ARCHIVED, _('ARCHIVED'))
    ]
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
    status = models.CharField(
        verbose_name=_('status'),
        choices=POST_STATUS_CHOICES,
        max_length=20,
        default=DRAFT
    )
    hits_counter = models.IntegerField(
        verbose_name=_('hits count'),
        default=0
    )
    revisions_counter = models.IntegerField(
        verbose_name=_('revisions count'),
        default=0
    )
    validated_at = models.DateTimeField(
        verbose_name=_('validated at'),
        unique=False,
        null=True,
        blank=False
    )
    validated_by = models.ForeignKey(
        to=Member,
        on_delete=models.DO_NOTHING,
        related_name="validated_by",
        null=True,
    )
    author = models.ForeignKey(
        to=Member,
        related_name='post_author',
        on_delete=models.CASCADE
    )
    readings = models.ManyToManyField(
        to=Member
    )
    book_part = models.ForeignKey(
        to=BookPart,
        related_name='book_part_ref',
        on_delete=models.CASCADE,
        null=True,
    )
    tags = models.ManyToManyField(
        to=Tag
    )
    revision = models.ForeignKey(
        to='self',
        related_name='revision_ref',
        on_delete=models.CASCADE,
        null=True
    )
    section = models.ForeignKey(
        to=Section,
        related_name='section_ref',
        on_delete=models.CASCADE
    )

    objects = PostManager()

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
