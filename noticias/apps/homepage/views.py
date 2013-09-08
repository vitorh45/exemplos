# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.contrib.comments.models import Comment
from django.core.cache import cache
from django.utils import simplejson
from articles.models import Article, Channel, Section
from videos.models import Video
from meuclick.models import ArticlesMeuClick
from blogs.models import Post,Blog
from clickweek.models import ClickWeek
from config.models import Config
#from utils.analytics import get_analytics_connection, filter_for_befts, get_filter_for_beft
from utils.dolar import getQuotation
from utils.mares import Mares
from datetime import datetime
import itertools
import urllib2


def index(request):    
    try:
        config = Config.objects.all()[0]
        config = config.len_panel
    except:
        config = 4
    article_urgente = Article.published_urgent.all()[:1]
    try:
        article_mega_manchete = Article.published.filter(is_mega_manchete=True)[0]
    except:
        article_mega_manchete = None
    articles_painel = Article.published.filter(section__slug='painel')[:config]
    articles_manchete = Article.published.filter(section__slug='manchete')[:4]
    articles_submanchete = Article.published.filter(section__slug='sub-manchete')[:4]
    articles_destaque = Article.published.filter(section__slug='destaques')[:4]
    articles_subdestaque_foto = Article.published.filter(section__slug='manchete')[4:7]
    articles_subdestaque_sem_foto = Article.published.filter(section__slug='sub-manchete')[4:7]
    articles_politica = Article.published.filter(channel__slug='politica')[:4]
    articles_tecnologia = Article.published.filter(channel__slug='tecnologia')[:4]
    articles_games = Article.published.filter(channel__slug='games')[:4]
    articles_humor = Article.published.filter(channel__slug='humor')[:4]

    articles_meuclick = ArticlesMeuClick.objects.all()[:4]

    clicksweek = ClickWeek.objects.all()[:9]
    clicks_semana = []
    clickstmp = []
    for i in range(0,len(clicksweek),3):
        try:
            clickstmp.append(clicksweek[i])
        except:
            pass
        try:
            clickstmp.append(clicksweek[i+1])
        except:
            pass
        try:
            clickstmp.append(clicksweek[i+2])
        except:
            pass
        clicks_semana.append(clickstmp)
        clickstmp = []

    #pegar dados de outro site
    articles_educacao = Article.published.filter(channel__slug='educacao')[:4]
    articles_saude = Article.published.filter(channel__slug='saude')[:4]
    cache_key_verychic = 'verychic-data-%s' %  datetime.now().strftime("%d-%m-%Y")
    article_verychic = cache.get(cache_key_verychic)
    cache_key_faro = 'faro-data-%s' %  datetime.now().strftime("%d-%m-%Y")
    articles_faro = cache.get(cache_key_faro)
    cache_key_clickchef = 'clickchef-data-%s' %  datetime.now().strftime("%d-%m-%Y")
    articles_clickchef = cache.get(cache_key_clickchef)
    articles_culinaria = Article.published.filter(channel__slug='culinaria')[:4]
    cache_key_befter = 'befter-data-%s' %  datetime.now().strftime("%d-%m-%Y")
    befter = cache.get(cache_key_befter)
    try:
        last_video = Video.objects.all()[0]
    except:
        last_video = None

    try:
        quotation = getQuotation()
    except:
        quotation = None

    try:
        mares = Mares()
    except:
        mares = None

    url_site = request.META.get('HTTP_HOST', '')
    return render_to_response('index.html', {
        'article_urgente':article_urgente,
        'article_mega_manchete':article_mega_manchete,
        'articles_painel':articles_painel,
        'articles_manchete':articles_manchete,
        'articles_submanchete':articles_submanchete,
        'articles_destaque':articles_destaque,
        'articles_subdestaque_foto':articles_subdestaque_foto,
        'articles_subdestaque_sem_foto': articles_subdestaque_sem_foto,
        'articles_politica':articles_politica,
        'articles_tecnologia':articles_tecnologia,
        'articles_games':articles_games,
        'articles_humor':articles_humor,
        'articles_saude':articles_saude,
        'articles_meuclick':articles_meuclick,
        #'article_verychic': article_verychic,
        'articles_faro':articles_faro,
        'articles_culinaria':articles_culinaria,
        'articles_educacao':articles_educacao,
        'clicks_semana':clicks_semana,
        #'befter':befter,
        'last_video':last_video,
        'quotation':quotation,
        'mares':mares.getMares(),
        'url_site':url_site,
    }, context_instance=RequestContext(request))


