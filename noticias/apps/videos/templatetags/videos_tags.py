#-*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings

from videos.models import Video

register = template.Library()

def do_get_videos_latest(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_videos_latest' tag takes exactly 4 arguments")
    return VideosLatestNode(bits[2],bits[3])

class VideosLatestNode(template.Node):
    def __init__(self, varname, num):
        self.varname = varname
        self.num = num
    def render(self, context):
        videos = Video.objects.all()[:self.num]
        context[self.varname] = videos
        return ''

def do_get_videos_most_viewed(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_videos_most_viewed' tag takes exactly 4 arguments")
    return VideosMostViewedNode(bits[2],bits[3])

class VideosMostViewedNode(template.Node):
    def __init__(self, varname, num):
        self.varname = varname
        self.num = num
    def render(self, context):
        videos = Video.objects.order_by('-views_count','-publication_date')[:self.num]
        context[self.varname] = videos
        return ''

register.tag('get_videos_most_viewed',do_get_videos_most_viewed)
register.tag('get_videos_latest',do_get_videos_latest)

