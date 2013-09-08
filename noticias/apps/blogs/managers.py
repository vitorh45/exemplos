# -*- coding: utf-8 -*-
from django.db import models

from datetime import datetime

class BlogPublishedManager(models.Manager):
    def get_query_set(self):
        return super(BlogPublishedManager, self).get_query_set(
        ).filter(
            enabled=True,
        )
        
class PostPublishedManager(models.Manager):
    def get_query_set(self):
        return super(PostPublishedManager, self).get_query_set(
        ).filter(
            blog__enabled=True,
            status='published',
            publication_date__lte=datetime.now()
        )
