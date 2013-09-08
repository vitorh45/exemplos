# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

class Poll(models.Model):

    title = models.CharField(u'Título', max_length=100)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    is_active = models.BooleanField(u'Ativar', default=False)
    # Audit fields
    created_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # Field to slug
    slug_field_name = 'slug'
    slug_from = 'title'

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Enquete'
        verbose_name_plural = u'Enquetes'
        ordering = ['-created_date']

class Choice(models.Model):

    poll = models.ForeignKey('Poll', verbose_name=u'Enquete')
    title = models.CharField(u'Escolha', max_length=200)
    votes = models.PositiveIntegerField(u'Votos', default=0)

