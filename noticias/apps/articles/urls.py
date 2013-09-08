from django.conf.urls.defaults import *

urlpatterns = patterns('articles.views',
    url(r'^ultimas/$', 'latest', name='articles_latest'),
    url(r'^mais-lidas/$', 'most_viewed', name='articles_most_viewed'),
    url(r'^mais-comentadas/$', 'most_commented', name='articles_most_commented'),    
    #url(r'^mais-enviadas/$', 'most_sent', name='most_sent'),
    url(r'^(?P<channel>[\w_-]+)/$', 'article_list', name='article_list'),
    url(r'^(?P<channel>[\w_-]+)/(?P<slug>[\w_-]+)/imprimir/$', 'article_print', name='article_print'),
    url(r'^(?P<channel>[\w_-]+)/(?P<slug>[\w_-]+)/imprimir/artigos/rss/index.xml/$', 'article_print_xml', name='article_print_xml'),
    url(r'^(?P<channel>[\w_-]+)/(?P<slug>[\w_-]+)/preview/$', 'article_preview', name='article_preview'),
    url(r'^(?P<channel>[\w_-]+)/(?P<slug>[\w_-]+)/$', 'article_show', name='article_show'),
)

