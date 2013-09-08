# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.comments.models import Comment

class CustomComment(Comment):

    class Meta:
        proxy = True
        verbose_name = u'comentário'
        verbose_name_plural = u'comentários'

