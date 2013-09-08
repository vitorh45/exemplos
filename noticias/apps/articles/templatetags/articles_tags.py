#-*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache
from django.contrib.comments.models import Comment
from django.db.models import Count
from articles.models import Article,Channel,Section
from datetime import datetime, timedelta
import re

register = template.Library()

def do_get_articles_latest(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_last_articles' tag takes exactly 4 arguments")
    return ArticlesLatestNode(bits[2],bits[3])

class ArticlesLatestNode(template.Node):
    def __init__(self, varname,num):
        self.varname = varname
        self.num = num
    def render(self, context):
        articles = Article.published.all()[:self.num]
        context[self.varname] = articles
        return ''

def do_get_all_channels(parser, token):

    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'get_last_articles' tag takes exactly 3 arguments")
    return AllChannelsNode(bits[2])

class AllChannelsNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        channels = Channel.objects.filter(enabled=True)
        context[self.varname] = channels
        return ''

def do_get_articles_most_viewed(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'get_articles_most_viewed' tag takes exactly 3 arguments")
    return ArticlesMostViewedNode(bits[2])

class ArticlesMostViewedNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        list_articles = []
        # cache_key_articles_last_week = 'articles-last-week-data-%s' %  datetime.now().strftime("%d-%m-%Y")
        # if not cache.get(cache_key_articles_last_week):
        list_articles = Article.published.all().order_by('-views_count_last_week')[:4]
        # else:
        #     articles = cache.get(cache_key_articles_last_week)
        #     for a in articles:
        #         try:
        #             article = Article.published.get(slug=a)
        #             list_articles.append(article)
        #         except:
        #             pass
        context[self.varname] = list_articles[:4]
        return ''

def do_get_articles_most_commented(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'get_articles_most_commented' tag takes exactly 3 arguments")
    return MostCommentedNode(bits[2])

class MostCommentedNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        seven_days_ago = datetime.now() - timedelta(days=7)
        articles_list = Article.published.filter(publication_date__gte=seven_days_ago).order_by('-comments_count')[:4]
        '''
        articles_list = []
        articles_most_commented = Comment.objects.filter(submit_date__gte=seven_days_ago).values('object_pk').annotate(counts=Count('object_pk')).order_by('-counts')[:4]
        for article in articles_most_commented:
            id_article =  article["object_pk"]
            try:
                articles_list.append(Article.published.get(id=id_article))
            except:
                pass
        '''
        context[self.varname] = articles_list
        return ''

def do_get_first_paragraph(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_first_paragraph' tag takes exactly 4 arguments")
    return FirstParagraphNode(bits[2],bits[3])

class FirstParagraphNode(template.Node):
    def __init__(self, varname, paragraph):
        self.varname = varname
        self.paragraph = template.Variable(paragraph)
    def render(self, context):
        paragraph = self.paragraph.resolve(context)
        p = re.compile(r'<[^<]*?/?>')
        p = p.sub('',paragraph)
        context[self.varname] = p.strip().split("\r\n")[0]
        return ''


register.tag('get_articles_latest',do_get_articles_latest)
register.tag('get_all_channels', do_get_all_channels)
register.tag('get_articles_most_viewed',do_get_articles_most_viewed)
register.tag('get_articles_most_commented', do_get_articles_most_commented)
register.tag('get_first_paragraph', do_get_first_paragraph)

