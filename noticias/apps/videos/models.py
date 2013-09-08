# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from tagging.fields import TagField
from apps.utils.youtube import service as youtube

class Video(models.Model):

    # Video title
    title = models.CharField(u'Título', max_length=100)
    # Video slug
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    # video headline
    headline = models.CharField(u'Manchete',max_length=100)
    # Video link
    id_video = models.CharField(u'Link do vídeo',max_length=200, help_text=u'formato do link: http://www.youtube.com/watch?v=Yw74sDWPH7U ou apenas o id do vídeo: Yw74sDWPH7U')
    # Video duration
    duration = models.CharField(u'Duração',max_length=15,editable=False)
    # Video content
    content = models.TextField(u'Conteúdo',blank=True,null=True)
    # Enable comments
    enable_comments = models.BooleanField(u'ativar comentários', default=True)
    # Video publication date
    publication_date = models.DateTimeField(u'Data da Publicação',
        default=datetime.now())
    # views count
    views_count = models.PositiveIntegerField(u'visitas',default=0, editable=False)
    # Video tags
    tags_string = TagField(u'tags', help_text=u'separar as tags por espaço. para tags com mais de uma palavra utilizar aspas duplas, exemplo: tag1 "tag2 tag2" tag3')
    # Audit fields
    created_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # Field to slug
    slug_field_name = 'slug'
    slug_from = 'title'

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'vídeo'
        verbose_name_plural = u'vídeos'
        ordering = ['-publication_date']
        get_latest_by = 'publication_date'

    def save(self,*args,**kwargs):
        # saving only the video id
        try:
            id_video = self.id_video.split("?v=")[1]
        except:
            id_video = self.id_video
        if "&" in id_video:
            id_video = id_video.split("&")[0]

        self.id_video = id_video
        #youtube
        yt_service = youtube.YouTubeService()
        entry = yt_service.GetYouTubeVideoEntry(video_id=self.id_video)
        duration = int(entry.media.duration.seconds)
        minutes = duration/60
        seconds = duration%60
        if seconds < 10:
            seconds = "0%s" % seconds
        self.duration = "%s:%s" % (minutes,seconds)

        super(Video,self).save(*args,**kwargs)

    def get_related_videos(self):
        """
        Return a max of 10 related entries to the instance entry.
        """
        most_similar = Video.tagged.with_all(self.tags).order_by('-publication_date')[:4]
        similar = Video.tagged.with_any(self.tags).order_by('-publication_date')[:7]

        related_videos = []

        for video in most_similar:
            related_videos.append(video)

        for video in similar:
            if not video in related_videos:
                related_videos.append(video)

        try:
            related_videos.remove(self)
        except ValueError:
            pass

        return related_videos[:3]

    @models.permalink
    def get_absolute_url(self):
        return ('video_show', (), {
            'slug': self.slug
        })

import tagging
try:
    tagging.register(Video)
except tagging.AlreadyRegistered:
    pass

