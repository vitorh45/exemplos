# -*- coding: utf-8 -*-
from django.db import models

from datetime import datetime

class ArticlePublishedManager(models.Manager):
    def get_query_set(self):
        return super(ArticlePublishedManager, self).get_query_set(
        ).select_related('channel', 'section').filter(
            status='published',
            channel__enabled=True,
            is_urgent=False,
            publication_date__lte=datetime.now()
        )

class ArticlePublishedDetailManager(models.Manager):
    def get_query_set(self):
        return super(ArticlePublishedDetailManager, self).get_query_set(
        ).select_related('channel', 'section').filter(
            status='published',
            channel__enabled=True,
            publication_date__lte=datetime.now()
        )

class ArticlePublishedUrgentManager(models.Manager):
    def get_query_set(self):
        return super(ArticlePublishedUrgentManager, self).get_query_set(
        ).select_related('channel', 'section').filter(
            status='published',
            channel__enabled=True,
            is_urgent=True,
            publication_date__lte=datetime.now()
        )

