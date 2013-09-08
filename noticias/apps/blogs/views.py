# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.core.cache import cache
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from apps.blogs.models import Blog, Post
from apps.utils.analytics import get_analytics_connection, get_filter_for_blog
from comments.forms import CommentForm
from datetime import datetime, timedelta
import traceback, sys

def blog_list(request):
    blogs = Blog.objects.filter(enabled=True)    
    return render_to_response('blog/blog_list.html', {
        'blogs': blogs,
    }, context_instance=RequestContext(request))

def blog_show(request, blog):    
    try:
        blog = Blog.objects.get(slug=blog, enabled=True)
    except:
        raise Http404(u'Página não encontrada')
    posts = Post.published.filter(blog=blog)    
    page = request.GET.get("page","1")
    return render_to_response('blog/blog_show.html', {
        'posts': posts,
        'blog':blog,
        'page':page,
    }, context_instance=RequestContext(request))

def blog_show_by_year(request, blog, year):    
    try:
        blog = Blog.objects.get(slug=blog)
    except:
        raise Http404(u'Página não encontrada')
    posts = Post.published.filter(Q(blog=blog) , Q(publication_date__year=year))
    page = request.GET.get("page","1")
    return render_to_response('blog/blog_show_year.html', {
        'posts': posts,
        'blog':blog,
        'date':year,
        'page':page,
    }, context_instance=RequestContext(request))

def blog_show_by_month(request, blog, year, month):    
    try:
        blog = Blog.objects.get(slug=blog)
    except:
        raise Http404(u'Página não encontrada')
    posts = Post.published.filter(Q(blog=blog) , Q(publication_date__year=year) , Q(publication_date__month=month))
    page = request.GET.get("page","1")
    return render_to_response('blog/blog_show_month.html', {
        'posts': posts,
        'blog':blog,
        'date':"%s/%s" % (month,year),
        'page':page,
    }, context_instance=RequestContext(request))

def post_show(request, blog, slug):    
    try:
        blog = Blog.objects.get(slug=blog)
    except:
        raise Http404(u'Não disponível')
    try:
        post = Post.published.get(slug=slug, blog=blog)
    except:
        raise Http404(u'Não disponível')    

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.submit_date = datetime.now()
            comment.user = None
            comment.site = Site.objects.get_current()
            comment.ip_address = request.META.get("REMOTE_ADDR", None)
            comment.content_type = ContentType.objects.get_for_model(post)
            comment.object_pk = post.id
            comment.save()
            return HttpResponseRedirect(reverse('post_show',args=(blog.slug,post.slug)))
    else:
        form = CommentForm()

    return render_to_response('blog/post_show.html', {
        'post': post,
        'blog': blog,
        'form':form,
    }, context_instance=RequestContext(request))

def post_print(request, blog, slug):    
    try:
        blog = Blog.objects.get(slug=blog)
    except:
        raise Http404(u'Não disponível')
    try:
        post = Post.published.get(slug=slug, blog=blog)
    except:
        raise Http404(u'Não disponível')
    return render_to_response('print/post_print.html', {
        'post': post,
    }, context_instance=RequestContext(request))

def latest(request):
    posts = Post.published.order_by('-publication_date')
    return render_to_response('blog/posts_latest.html', {
        'posts': posts,
    }, context_instance=RequestContext(request))

def most_viewed(request):
    posts = Post.published.order_by('-views_count')
    return render_to_response('blog/posts_most_viewed.html', {
        'posts': posts,
    }, context_instance=RequestContext(request))


