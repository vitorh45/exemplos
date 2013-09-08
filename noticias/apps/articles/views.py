# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.template import RequestContext
from django.contrib.comments.models import Comment
from django.core.cache import cache
from django.utils import simplejson
from django.db.models import Count
from django.db.models import Q
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from apps.articles.models import Article, Channel, Section
from comments.forms import CommentForm
from apps.utils.analytics import get_analytics_connection, get_filter_for_article
from datetime import datetime, timedelta
import traceback, sys

def latest(request):
    articles = Article.published.order_by('-publication_date')
    page = request.GET.get("page","1")
    return render_to_response('articles/articles_latest.html', {
        'articles': articles,
        'page':page,
    }, context_instance=RequestContext(request))

def most_viewed(request):
    articles = Article.published.order_by('-views_count')
    page = request.GET.get("page","1")
    return render_to_response('articles/articles_most_viewed.html', {
        'articles': articles,
        'page':page,
    }, context_instance=RequestContext(request))

def most_commented(request):
    articles_list = []
    articles_list = Article.published.order_by('-comments_count')    
    page = request.GET.get("page","1")
    return render_to_response('articles/articles_most_commented.html', {
        'articles': articles_list,
        'page':page,
    }, context_instance=RequestContext(request))

def article_list(request,channel):    
    articles = Article.published.filter(channel__slug=channel)
    try:
        channel = Channel.objects.get(slug=channel).name
    except:
        raise Http404(u'Não disponível')
    page = request.GET.get("page","1")
    return render_to_response('articles/article_list.html', {
        'channel':channel,
        'articles': articles,
        'page':page,
    }, context_instance=RequestContext(request))

def article_show(request, channel, slug):
    try:
        article = Article.published_detail.get(slug=slug, channel__slug=channel)
        article.views_count_last_week += 1
        article.views_count += 1
        article.save()
    except:
        raise Http404(u'Notícia não encontrada')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.submit_date = datetime.now()
            comment.user = None
            comment.site = Site.objects.get_current()
            comment.ip_address = request.META.get("REMOTE_ADDR", None)
            comment.content_type = ContentType.objects.get_for_model(article)
            comment.object_pk = article.id
            comment.save()
            return HttpResponseRedirect(reverse('article_show',args=(article.channel.slug,article.slug)))
    else:
        form = CommentForm()

    related_articles = article.get_related_articles()
    return render_to_response('articles/article_show.html', {
        'article': article,
        'related_articles': related_articles,
        'form':form,
        'is_article':True,
    }, context_instance=RequestContext(request))

def article_print(request, channel, slug):
    try:
        article = Article.published.get(slug=slug, channel__slug=channel)
    except:
        raise Http404(u'Não disponível')
    return render_to_response('print/article_print.html', {
        'article': article,
    }, context_instance=RequestContext(request))

def article_print_xml(request, channel, slug):
    return HttpResponsePermanentRedirect(
            reverse('article_show', args=[channel,slug])
        )

def article_preview(request, channel, slug):
    try:
        article = Article.objects.get(slug=slug, channel__slug=channel)
    except:
        raise Http404(u'Notícia não encontrada')

    return render_to_response('articles/article_preview.html', {
        'article': article,
    }, context_instance=RequestContext(request))

def search(request):
    term = request.GET.get('q', '')
    page = request.GET.get('page','1')
    articles = Article.published_detail.filter(Q(title__icontains=term) | Q(title_secondary__icontains=term) | Q(summary__icontains=term) | Q(content__icontains=term)  )
    return render_to_response('articles/search.html', {
        'articles': articles,
        'term':term,
        'page':page,
    }, context_instance=RequestContext(request))


    data = simplejson.dumps({'success':True}, indent=2, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/javascript; charset=utf8')

def decrement_comments(request,slug):
    try:
        article = Article.objects.get(slug=slug)
        article.comments_count -= 1
        article.save()
    except:
        pass
    data = simplejson.dumps({'success':True}, indent=2, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/javascript; charset=utf8')

