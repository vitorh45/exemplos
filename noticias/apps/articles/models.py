# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.fields.files import ImageFieldFile
from tagging.fields import TagField
from datetime import datetime
from articles.managers import ArticlePublishedManager, ArticlePublishedUrgentManager, ArticlePublishedDetailManager
from meuclick.models import UserMeuClick
from registration.utils import EmailThread
from apps.utils.images import crop_center, add_file_termination
import Image
from os.path import splitext, split, join

from djangosphinx.models import SphinxSearch

def content_file_name(instance, filename):
    path, file_name = split(filename)
    file_name, ext = splitext(file_name)
    month, year = datetime.now().strftime("%m/%Y").split("/")
    return '/'.join(['images/dynamic/articles/%s/%s' % (year,month), instance.slug+ext])

class Channel(models.Model):
    # Channel name
    name = models.CharField(u'Nome', max_length=100, unique=True)
    # Channel slug
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    # Flag to enable this channel
    enabled = models.BooleanField(u'ativado', default=True, db_index=True)
    # Id from legacy
    id_migration = models.PositiveIntegerField(default=0, db_index=True)
    # Audit fields
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # Field to slug
    slug_field_name = 'slug'
    slug_from = 'name'

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'canal'
        verbose_name_plural = u'canais'


class Section(models.Model):
    # Section Name
    name = models.CharField(u'Nome', max_length=100, unique=True)
    # Section slug
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    # Flag to enable this section
    enabled = models.BooleanField(default=True, db_index=True)
    # Id from legacy
    id_migration = models.PositiveIntegerField(default=0, db_index=True)
    # Audit fields
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # Field to slug
    slug_field_name = 'slug'
    slug_from = 'name'

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'seção'
        verbose_name_plural = u'seções'

class Article(models.Model):
    # Status choices
    STATUS_CHOICES = (
        ('published', u'Publicado'),
        ('draft', u'Rascunho'),
        ('pending', u'Pendente'),
    )
    # Article Owner
    user = models.ForeignKey(User, related_name=u'articles',
        verbose_name=u'Usuário')
    # Article Channel
    channel = models.ForeignKey(Channel, related_name=u'channels',
        verbose_name=u'Canal')
    # Article Section
    section = models.ForeignKey(Section, related_name=u'sections',
        verbose_name=u'Seção', blank=True, null=True)
    # Article Title
    title = models.CharField(u'Título fora', max_length=200,
        help_text=u'máximo de 70 caracteres.')
    # Article title in the detail page
    title_secondary = models.CharField(u'Título dentro', max_length=250,
        blank=True, null=True)
    # Article Slug
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    # Article Headline
    headline = models.CharField(u'Subtítulo', max_length=40, blank=True,
        help_text=u'máximo de 40 caracteres')
    # Article Summary
    summary = models.CharField(u'Resumo', max_length=160, blank=True,
        help_text=u'máximo de 160 caracteres')
    # Article Content
    content = models.TextField(u'Conteúdo')
    # Article Source and Source url
    source = models.CharField(u'Fonte', max_length=255, blank=True)
    source_url = models.CharField(u'URL da Fonte', max_length=255, blank=True)
    # Article author
    author = models.CharField(u'Autor', max_length=255, blank=True)
    #Article picture
    picture = models.ImageField('Imagem',
        upload_to=content_file_name,max_length=300, blank=True)
    # picture subtitle
    picture_subtitle = models.CharField(u'Legenda da imagem', max_length=50,
        blank=True, null=True)
    # picture cropped for the iphone
    picture_cropped = models.ImageField(editable=False,
        upload_to='images/dynamic/articles/%Y/%m/', max_length=400, null=True,
        blank=True)
    # Status
    status = models.CharField(u'Status', max_length=10, choices=STATUS_CHOICES,
        default='draft', db_index=True)
    # views count
    views_count = models.PositiveIntegerField('Número de visitas',
        editable=False, default=0, db_index=True)
    # views count
    views_count_last_week = models.PositiveIntegerField('Número de visitas nos últimos sete dias',
        editable=False, default=0, db_index=True)
    # Publication date and hour
    publication_date = models.DateTimeField(u'Data da Publicação',
        default=datetime.now, db_index=True)
    # articles usermeuclick. used when the article come from an article sent by an usermeuclick
    usermeuclick = models.ForeignKey(UserMeuClick, verbose_name=u'Usuário vcnoclick', null=True, blank=True, help_text=u'Selecione algum valor somente se a notícia foi enviada por algum usuário.')
    # Is Urgent
    is_urgent = models.BooleanField(u'ativar notícia urgente', default=False,
        db_index=True)
    is_mega_manchete = models.BooleanField(u'ativar notícia mega manchete', default=False,
        db_index=True)
    # Enable comments
    enable_comments = models.BooleanField(u'ativar comentários', default=True)
    comments_count = models.PositiveIntegerField(u'Número de comentários', default=0, editable=False)
    # Created date and hour
    created_date = models.DateTimeField(u'Data da Criação',
        default=datetime.now, editable=False)
    # Id from clickpb
    id_migration = models.CharField(max_length=15, db_index=True, editable=False,
        default='0')
    # Video tags
    tags_string = TagField(u'tags', help_text=u'separar as tags por espaço. para tags com mais de uma palavra utilizar aspas duplas, exemplo: tag1 "tag2 tag2" tag3')
    # Slug
    slug_field_name = 'slug'
    slug_from = 'title'
    # managers
    objects = models.Manager()
    published = ArticlePublishedManager()
    published_detail = ArticlePublishedDetailManager()
    published_urgent = ArticlePublishedUrgentManager()

    search = SphinxSearch('articles')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'artigo'
        verbose_name_plural = u'artigos'
        ordering = ['-publication_date']

    def save(self, *args, **kwargs):
        super(Article,self).save(*args, **kwargs)
        try:
            img = Image.open(self.picture)
            img.thumbnail((110,100000000), Image.ANTIALIAS)
            img = crop_center(img, (103,77))
            name = add_file_termination(self.picture.name, '_crop')
            path = add_file_termination(self.picture.path, '_crop')
            self.picture_cropped = ImageFieldFile(self,self.picture_cropped, name)
            img.save(self.picture_cropped.path, quality=100)
            super(Article,self).save(*args, **kwargs)
        except:
            pass
        if self.usermeuclick:
            print "ok"

    def get_related_articles(self):
        most_similar = Article.tagged.with_all(self.tags).order_by('-publication_date')[:6]
        similar = Article.tagged.with_any(self.tags).order_by('-publication_date')[:11]
        related_articles = []
        for article in most_similar:
            related_articles.append(article)
        for article in similar:
            if not article in related_articles:
                related_articles.append(article)
        try:
            related_articles.remove(self)
        except ValueError:
            pass
        return related_articles[:5]

    @models.permalink
    def get_absolute_url(self):
        return ('article_show', (), {
        'channel': self.channel.slug,
        'slug': self.slug})

import tagging
try:
    tagging.register(Article)
except tagging.AlreadyRegistered:
    pass

