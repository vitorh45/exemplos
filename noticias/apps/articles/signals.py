# -*- coding: utf-8 -*-
from django.db.models import signals
from django.db.models.signals import post_save
from django.db.models import get_model
from django.conf import settings
#from varnishapp.manager import manager
from articles.models import Article


#def absolute_url_purge_handler(sender, **kwargs):
#    manager.run('purge.url', r'^/$')

#if settings.ENABLE_DJANGO_VARNISH:
#    post_save.connect(absolute_url_purge_handler, sender=Article)

