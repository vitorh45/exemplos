# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageFieldFile
from datetime import datetime
from apps.utils.images import crop_center, add_file_termination
import Image
from blogs.managers import BlogPublishedManager, PostPublishedManager

class Blog(models.Model):
    # Blog owner
    user = models.OneToOneField(User, verbose_name=u'Usuário',
        related_name='blog', editable=False)
    # Blog title
    title = models.CharField(u'Título', max_length=250)
    # Blog slug
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    # Blog description
    description = models.TextField(u'Descrição', blank=True)
    # blog picture
    picture = models.ImageField(u'Imagem grande',upload_to='images/dynamic/images_blog')
    # blog picture_small user in the sidebar
    picture_small = models.ImageField(u'Imagem pequena',upload_to='images/dynamic/images_blog', blank=True, null=True)
    # blog picture_cropped user in the iphone
    picture_cropped = models.ImageField(editable=False,upload_to='images/dynamic/images_blog', null=True)
    # twitter
    twitter_username = models.CharField(u'Twitter',max_length=50, blank=True, null=True)
    # blog order
    order = models.PositiveIntegerField(u'Ordenação', default=0, help_text='1 é a posição mais elevada.')
    # blog highlight
    is_highlight = models.BooleanField(u'Ativar como destaque', default=False)
    # Enable flag
    enabled = models.BooleanField(u'Ativado', default=True, db_index=True)
    # Audit fields
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # Field to slug
    slug_field_name = 'slug'
    slug_from = 'title'
    # managers
    objects = models.Manager()
    published = BlogPublishedManager()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'colunista'
        verbose_name_plural = u'colunistas'
        ordering = ['order']

    def save(self, *args, **kwargs):
        super(Blog,self).save(*args, **kwargs)
        try:
            img = Image.open(self.picture_small)
            img.thumbnail((130,100000000), Image.ANTIALIAS)
            img = crop_center(img, (103,77))
            name = add_file_termination(self.picture.name, '_crop')
            path = add_file_termination(self.picture.path, '_crop')
            self.picture_cropped = ImageFieldFile(self,self.picture_cropped, name)
            img.save(self.picture_cropped.path, quality=100)
            super(Blog,self).save(*args, **kwargs)
        except:
            pass

#class Post(EnableAuditModel, EnableTagModel, EnableSlugModel, EnableCommentsModel, EnableStatusModel):
class Post(models.Model):
    # Status choices
    STATUS_CHOICES = (
        ('published', u'Publicado'),
        ('draft', u'Rascunho'),
        ('pending', u'Pendente'),
    )
    # Blog
    blog = models.ForeignKey(Blog, verbose_name=u'blog', related_name='posts',
        editable=False)
    # Post owner
    user = models.ForeignKey(User, verbose_name=u'Usuário',
        related_name='posts', editable=False)
    # Post title
    title = models.CharField(u'Título', max_length=200)
    # Post slug
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    # Post content
    content = models.TextField(u'Conteúdo',blank=True,null=True)
    # Status
    status = models.CharField(u'Status', max_length=10, choices=STATUS_CHOICES, default='draft', db_index=True)
    # views counts
    views_count = models.PositiveIntegerField(editable=False, default=0, db_index=True)
    # Enable comments
    enable_comments = models.BooleanField(u'ativar comentários', default=True)
    comments_count = models.PositiveIntegerField(u'Número de comentários',default=0,editable=False)
    # Post publication date
    publication_date = models.DateTimeField(u'Data da Publicação',
        default=datetime.now)
    # Audit fields
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # Field to slug
    slug_field_name = 'slug'
    slug_from = 'title'
    # managers
    objects = models.Manager()
    published = PostPublishedManager()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'post'
        verbose_name_plural = u'posts'
        ordering = ['-publication_date']
        get_latest_by = 'publication_date'

    @models.permalink
    def get_absolute_url(self):
        return ('post_show', (), {
        'blog': self.blog.slug,
        'slug': self.slug})

