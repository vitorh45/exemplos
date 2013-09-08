# -*- coding: utf-8 -*-
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.utils import simplejson
from django.db.models import Q
from django.utils.safestring import mark_safe, SafeData
from articles.models import Article
from blogs.models import Blog, Post
from videos.models import Video
from clickweek.models import ClickWeek
import datetime

def news_list_by_category(request, channel):

    json_output = []
    if channel == "home":
        articles = Article.published_detail.filter(section__slug='manchete')[:10]
    else:
        articles = Article.published_detail.filter(channel__slug=channel)[:10]

    for article in articles:
        if article.picture_cropped:
            picture = "http://"+request.META['HTTP_HOST']+article.picture_cropped.url
        else:
            picture = None
        json_output.append(
            {
                'title': article.title,
                'title_secondary': article.title_secondary,
                'slug': article.slug,
                'headline': article.headline,
                'publication_date': article.publication_date.strftime("%d/%m/%Y - %H:%M"),
                'picture':picture,
                'content':article.content,
                'url': "http://"+request.META['HTTP_HOST']+"/noticias/"+article.channel.slug+"/"+article.slug
            }
        )

    data = simplejson.dumps(json_output, indent=2, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/javascript; charset=utf8')

def news_list_most_viewed(request):

    json_output = []
    articles = Article.published_detail.order_by('-views_count','publication_date')[:10]

    for article in articles:
        if article.picture_cropped:
            picture = "http://"+request.META['HTTP_HOST']+article.picture_cropped.url
        else:
            picture = None
        json_output.append(
            {
                'title': article.title,
                'title_secondary': article.title_secondary,
                'slug': article.slug,
                'headline': article.headline,
                'publication_date': article.publication_date.strftime("%d/%m/%Y - %H:%M"),
                'picture':picture,
                'content':article.content,
                'url': "http://"+request.META['HTTP_HOST']+"/noticias/"+article.channel.slug+"/"+article.slug
            }
        )

    data = simplejson.dumps(json_output, indent=2, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/javascript; charset=utf8')

def news_list_latest(request):

    json_output = []
    articles = Article.published_detail.all()[:10]
    for article in articles:
        if article.picture_cropped:
            picture = "http://"+request.META['HTTP_HOST']+article.picture_cropped.url
        else:
            picture = None
        json_output.append(
            {
                'title': article.title,
                'title_secondary': article.title_secondary,
                'slug': article.slug,
                'headline': article.headline,
                'publication_date': article.publication_date.strftime("%d/%m/%Y - %H:%M"),
                'picture':picture,
                'content':article.content,
                'url': "http://"+request.META['HTTP_HOST']+"/noticias/"+article.channel.slug+"/"+article.slug
            }
        )

    data = simplejson.dumps(json_output, indent=2, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/javascript; charset=utf8')

def video_list(request):

    json_output = []
    videos = Video.objects.all()[:10]

    for video in videos:
        youtube = '<object width="144" height="108"><param name="movie" value="http://www.youtube.com/v/%s?fs=1&amp;hl=pt_BR"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/%s?fs=1&amp;hl=pt_BR" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="144" height="108"></embed></object>' % (video.id_video,video.id_video)

        json_output.append(
            {
                'title': video.title,
                'slug': video.slug,
                'headline': video.headline,
                'id_video': video.id_video,
                'youtube': youtube,
                'duration': video.duration,
                'publication_date': video.publication_date.strftime("%d/%m/%Y - %H:%M"),
                #2'picture':article.picture,
                'content':video.content,
            }
        )

    data = simplejson.dumps(json_output, indent=2, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/javascript; charset=utf8')

def blog_list(request):

    json_output = []
    blogs = Blog.published.all()

    for blog in blogs:
        last_post = Post.published.filter(blog=blog).latest()
        try:
            picture = "http://"+request.META['HTTP_HOST']+blog.picture_cropped.url
        except:
            picture = None
        json_output.append(
            {
                'name': blog.title,
                'slug': blog.slug,
                'description': blog.description,
                'picture': picture,
                'twitter':blog.twitter_username,
                'title': last_post.title,
                'content': last_post.content,
                'publication_date': last_post.publication_date.strftime("%d/%m/%Y - %H:%M"),
                'url': "http://"+request.META['HTTP_HOST']+"/colunas/"+blog.slug+"/"+last_post.slug
            }
        )
    data = simplejson.dumps(json_output, indent=2, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/javascript; charset=utf8')

def blog_show(request,blog):

    json_output = []
    posts = Post.published.filter(blog__slug=blog)[:10]
    for post in posts:
        json_output.append(
            {
                'title': post.title,
                'slug': post.slug,
                'content': post.content,
                'publication_date': post.publication_date.strftime("%d/%m/%Y - %H:%M"),
                'picture': None,
                'url': "http://"+request.META['HTTP_HOST']+"/colunas/"+blog+"/"+post.slug
            }
        )
    data = simplejson.dumps(json_output, indent=2, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/javascript; charset=utf8')


def clickweek_list(request):

    json_output = []

    clicksweek = ClickWeek.objects.all()
    for clickweek in clicksweek:
        if clickweek.picture_medium and clickweek.picture_small :
            picture = "http://"+request.META['HTTP_HOST']+clickweek.picture.url
            picture_small = "http://"+request.META['HTTP_HOST']+clickweek.picture_small.url
            picture_medium = "http://"+request.META['HTTP_HOST']+clickweek.picture_medium.url
        else:
            picture_small = None
            picture_medium = None
        json_output.append(
            {
                'title': clickweek.title,
                'slug': clickweek.slug,
                'publication_date': clickweek.publication_date.strftime("%d/%m/%Y - %H:%M"),
                'picture': picture,
                'picture_small':picture_small,
                'picture_medium':picture_medium,
            }
        )

    data = simplejson.dumps(json_output, indent=2, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/javascript; charset=utf8')

def search(request):
    try:
        term = request.GET['term']
    except:
        term = ''
    json_output = []
    articles = Article.published_detail.filter(Q(title__icontains=term) | Q(title_secondary__icontains=term) | Q(headline__icontains=term) | Q(summary__icontains=term) | Q(content__icontains=term))[:10]
    for article in articles:
        if article.picture_cropped:
            picture = "http://"+request.META['HTTP_HOST']+article.picture_cropped.url
        else:
            picture = None

        json_output.append(
            {
                'title': article.title,
                'title_secondary': article.title_secondary,
                'slug': article.slug,
                'headline': article.headline,
                'publication_date': article.publication_date.strftime("%d/%m/%Y - %H:%M"),
                'picture':picture,
                'content':article.content,
                'url': "http://"+request.META['HTTP_HOST']+"/noticias/"+article.channel.slug+"/"+article.slug
            }
        )

    data = simplejson.dumps(json_output, indent=2, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/javascript; charset=utf8')

