from datetime import datetime
from django.db import models

from .fields import ImageWithThumbsField
from . import listeners
from . import managers
from . import settings


class Tag(models.Model):
    slug = models.SlugField(
        db_index=True)
    tag = models.CharField(
        max_length=255)

    objects = managers.TagManager()

    def __unicode__(self):
        return u'%s' % self.tag

    @models.permalink
    def get_absolute_url(self):
        return ('omblog:tag', (), {
            'slug': self.slug,
        })


class Post(models.Model):
    PUBLISHED = 3
    HIDDEN = 4
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (HIDDEN, 'Hidden'),
    )
    title = models.CharField(
        max_length=255)
    slug = models.SlugField(
        db_index=True,
        unique=True,
        max_length=255)
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    source_content = models.TextField(
        'content',
        blank=True,
        null=True)
    rendered_content = models.TextField(
        blank=True,
        null=True)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=HIDDEN)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        null=True)
    created = models.DateTimeField(
        blank=True,
        null=True)

    objects = managers.PostManager()

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('omblog:post', (), {
            'slug': self.slug,
        })

    @models.permalink
    def edit_url(self):
        return ('omblog:edit', (), {
            'pk': self.pk,
        })

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()
        super(Post, self).save(*args, **kwargs)


class PostImage(models.Model):
    post = models.ForeignKey(Post)
    src = ImageWithThumbsField(
        upload_to='%Y/%m/%d/omblog',
        sizes=settings.IMAGE_SIZES,
        blank=True,
        null=True)
    created = models.DateTimeField(
        auto_now_add=True)
    title = models.CharField(
        blank=True,
        null=True,
        max_length=255)

    def __unicode__(self):
        return u'%s' % self.title or self.src

    def large(self):
        return self.src.url_900x600

    def thumb(self):
        return self.src.url_320x240


models.signals.pre_save.connect(
    listeners.clear_cached_posts,
    sender=Post,
    dispatch_uid='clear_cached_posts')

models.signals.pre_save.connect(
    listeners.post_date,
    sender=Post,
    dispatch_uid='post_date')

models.signals.pre_save.connect(
    listeners.post_create_slug,
    sender=Post,
    dispatch_uid='post_create_slug')

models.signals.pre_save.connect(
    listeners.post_render_content,
    sender=Post,
    dispatch_uid='post_render_content')
