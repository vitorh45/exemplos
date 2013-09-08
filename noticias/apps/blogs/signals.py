# -*- coding: utf-8 -*-
from django.db.models import signals
from django.template.defaultfilters import slugify

from blog.models import Blog, Post

def create_slug(sender, instance, signal, *args, **kwargs):
   if not instance.slug:
      instance.slug = slugify(getattr(instance, instance.slug_from))
      instance.save()

# post_save signals
signals.post_save.connect(create_slug, sender=Blog)
signals.post_save.connect(create_slug, sender=Post)

