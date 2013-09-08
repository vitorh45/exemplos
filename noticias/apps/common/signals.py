# -*- coding: utf-8 -*-
from django.db.models import signals
from django.template.defaultfilters import slugify
from django.contrib.comments import Comment
from common.utils import unique_slugify
from articles.models import Channel, Section, Article
from blogs.models import Blog, Post
from videos.models import Video
from clickweek.models import ClickWeek
from polls.models import Poll

def create_slug(sender, instance, signal, *args, **kwargs):
    if not instance.slug:
        unique_slugify(instance, getattr(instance, instance.slug_from))

# post_save signals
signals.pre_save.connect(create_slug, sender=Channel)
signals.pre_save.connect(create_slug, sender=Section)
signals.pre_save.connect(create_slug, sender=Article)
signals.pre_save.connect(create_slug, sender=Blog)
signals.pre_save.connect(create_slug, sender=Post)
signals.pre_save.connect(create_slug, sender=Video)
signals.pre_save.connect(create_slug, sender=ClickWeek)
signals.pre_save.connect(create_slug, sender=Poll)


def comment_moderation(sender, instance, signal, *args, **kwargs):
    if not instance.id:
        instance.is_public = False
signals.pre_save.connect(comment_moderation, sender=Comment)

