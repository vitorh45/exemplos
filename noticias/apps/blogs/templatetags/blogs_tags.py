#-*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from blogs.models import Blog, Post
from datetime import datetime
from django.utils.encoding import smart_str, smart_unicode

register = template.Library()

def do_get_blog_list(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'get_list_blogs' tag takes exactly 3 arguments")
    return ListBlogNode(bits[2])

class ListBlogNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        blogs = Blog.published.filter(is_highlight=True)
        try:
            blog_not_highlight = Blog.published.filter(is_highlight=False).order_by('?')[0]
        except:
            blog_not_highlight = None
        context[self.varname] = blogs
        return ''

def do_get_blog_not_highlight(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'get_blog_not_highlight' tag takes exactly 3 arguments")
    return BlogNotHighlightNode(bits[2])

class BlogNotHighlightNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        try:
            blog = Blog.published.filter(is_highlight=False).order_by('?')[0]
        except:
            blog = None
        context[self.varname] = blog
        return ''

def do_get_last_post(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_list_blogs' tag takes exactly 4 arguments")
    return LastPostNode(bits[2],bits[3])

class LastPostNode(template.Node):
    def __init__(self, varname,blog):
        self.varname = varname
        self.blog = template.Variable(blog)
    def render(self, context):

        blog = self.blog.resolve(context)
        try:
            last_post = Post.published.filter(blog__slug=blog)[0]
        except:
            last_post = None
        context[self.varname] = last_post
        return ''

def do_get_months(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_list_blogs' tag takes exactly 4 arguments")
    return MonthsNode(bits[2],bits[3])

class MonthsNode(template.Node):
    def __init__(self, varname,slug):
        self.varname = varname
        self.slug = template.Variable(slug)
    def render(self, context):
        slug = self.slug.resolve(context)
        blog = Blog.objects.get(slug=slug)
        posts = Post.objects.filter(Q(blog=blog), Q(blog__enabled=True), Q(status='published'),Q(publication_date__lte=datetime.now()))
        months = list(posts.dates("publication_date", "month", order="ASC"))
        context[self.varname] = months

        return ''

def do_get_posts_most_viewed(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'get_posts_most_viewed' tag takes exactly 3 arguments")
    return PostsMostViewedNode(bits[2])

class PostsMostViewedNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        list_posts = []
        cache_key_posts_last_week = 'posts-last-week-data-%s' %  datetime.now().strftime("%d-%m-%Y")
        if not cache.get(cache_key_posts_last_week):
            list_posts = Post.published.all()[:4]
        else:
            posts = cache.get(cache_key_posts_last_week)
            for a in posts:
                try:
                    post = Post.published.get(slug=a["slug"])
                    list_posts.append(post)
                except:
                    pass
        context[self.varname] = list_posts
        return ''


def do_get_posts_most_viewed_by_blog(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_posts_most_viewed' tag takes exactly 4 arguments")
    return PostsMostViewedByBlogNode(bits[2],bits[3])

class PostsMostViewedByBlogNode(template.Node):
    def __init__(self, varname, blog):
        self.varname = varname
        self.blog = template.Variable(blog)
    def render(self, context):
        blog = self.blog.resolve(context)
        posts = Post.published.filter(blog=blog).order_by('-views_count')[:4]
        context[self.varname] = posts
        return ''

def do_get_posts_latest(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'get_posts_latest' tag takes exactly 3 arguments")
    return PostsLatestNode(bits[2])

class PostsLatestNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        posts = Post.published.all()[:4]
        context[self.varname] = posts
        return ''

def do_title(parser, token):
    tag_name, title_string = token.split_contents()
    return TitleNode(title_string)

class TitleNode(template.Node):
    def __init__(self,title_string):
        self.title_string = template.Variable(title_string)
    def render(self, context):
        titulo = self.title_string.resolve(context).split(" ")
        list_names = ""
        for t in range(len(titulo)):
            if t%2 == 0 :
                list_names += smart_str(titulo[t])+""
            else:
                list_names += "<b>"+smart_str(titulo[t])+"</b>"
        return list_names

register.tag('get_last_post', do_get_last_post)
register.tag('get_blog_list', do_get_blog_list)
register.tag('get_blog_not_highlight', do_get_blog_not_highlight)
register.tag('get_months', do_get_months)
register.tag('get_posts_most_viewed', do_get_posts_most_viewed)
register.tag('get_posts_most_viewed_by_blog', do_get_posts_most_viewed_by_blog)
register.tag('get_posts_latest', do_get_posts_latest)
register.tag('do_title', do_title)

