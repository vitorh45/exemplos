from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.contrib.sitemaps import FlatPageSitemap
from homepage.views import index, view_as_browser, view_as_mobile, get_data, session_items, clear_session
from articles.views import search
from articles.models import Article
from blogs.models import Post
from videos.models import Video

from datetime import datetime, date

from sitemaps import LimitedSitemap

admin.autodiscover()

# sitemaps
articles_dict = {
    'queryset': Article.published.all(),
    'date_field': 'publication_date',
}
posts_dict = {
    'queryset': Post.published.all(),
    'date_field': 'publication_date',
}
videos_dict = {
    'queryset': Video.objects.order_by('-publication_date'),
    'date_field': 'publication_date',
}
sitemaps = {
    'flatpages': FlatPageSitemap,
    'articles': LimitedSitemap(articles_dict, priority=0.5),
    'posts': LimitedSitemap(posts_dict, priority=0.5),
    'videos': LimitedSitemap(videos_dict, priority=0.5),
}

urlpatterns = patterns('',
    # Example:
    # (r'^clickpb/', include('clickpb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # grappelli urls
    (r'^grappelli/', include('grappelli.urls')),

    # filebrowser urls
    (r'^admin/filebrowser/', include('filebrowser.urls')),

    # index
    url(r'^$', index, name="index"),
    url(r'^get_data/$', get_data, name="get_data"),

    # articles app
    (r'^noticias/', include('articles.urls')),
    url(r'^get_articles_visits/$', 'articles.views.get_articles_visits', name="get_articles_visits"),
    # articles redirect
    url(r'^artigo.php/$', 'articles.views.article_redirect', name='articles_redirect'),
    url(r'^~clickpb/artigo.php/$', 'articles.views.article_redirect', name='articles_redirect'),
    url(r'^clickpb/artigo.php/$', 'articles.views.article_redirect', name='articles_redirect'),
    url(r'^artigo2.php/$', 'articles.views.article_redirect', name='articles_redirect'),
    url(r'^canal.php/$', 'articles.views.channel_redirect', name='channels_redirect'),
    url(r'^arquivo.php/$', 'articles.views.arquivo_redirect', name='arquivo_redirect'),

    #  search
    url(r'^buscar/$', search ,name="search"),

    # blogs app
    (r'^colunistas/', include('blogs.urls')),
    url(r'^blog.php/$', 'blogs.views.redirect', name='blogs_redirect'),
    url(r'^get_posts_visits/$', 'blogs.views.get_posts_visits', name="get_posts_visits"),

    # videos app
    (r'^videos/', include('videos.urls')),

    # clickweek app
    (r'^cliques-da-semana/', include('clickweek.urls')),

    # contact app
    (r'^contato/', include('contact.urls')),

    # Feeds app urls
    (r'^feeds/', include('feeds.urls')),

    # polls app
    (r'^enquete/', include('polls.urls')),

    # water url
    url(r'^mares/$', direct_to_template ,{'template':'water/water.html'}, name='water'),

    # registration app
    url(r'^vcnoclick/acessar/$', 'meuclick.views.access',name="vcnoclick_acessar"),
    url(r'^vcnoclick/enviar-noticia/$', 'meuclick.views.send',name="vcnoclick_enviar"),
    url(r'^vcnoclick/cadastro/ok/$', direct_to_template ,{'template':'meuclick/register_ok.html'}, name="register_ok"),
    url(r'^vcnoclick/cadastro/ativacao/(?P<token>[\w_-]+)/$', 'meuclick.views.register_activation', name="register_activation"),
    url(r'^vcnoclick/cadastro/resetar-senha/$', 'meuclick.views.reset_password', name="reset_password"),
    url(r'^vcnoclick/cadastro/resetar-senha/(?P<token>[\w_-]+)/$', 'meuclick.views.reset_password_form', name="reset_password_form"),    url(r'^vcnoclick/logout/$', 'meuclick.views.logout', name="logout"),

    # meuclick app
    #(r'^meuclick/', include('meuclick.urls')),
    #url(r'^vcnoclick-login/$', direct_to_template ,{'template':'meuclick/login.html'}, name='form'),
    #url(r'^vcnoclick-enviar/$', direct_to_template ,{'template':'meuclick/enviar.html'}, name='enviar'),

    #comments app from django.contrib
    (r'^comentarios/', include('django.contrib.comments.urls')),

    # captcha url
    url(r'^captcha/', include('captcha.urls')),

    # api mobile
    (r'^api/', include('api.urls')),

    # mobile urls
    # change to view the site as a desktop browser
    url(r'^view_as_browser/$',view_as_browser, name='view_as_browser'),
    # change to view the site as a mobile browser
    url(r'^view_as_mobile/$',view_as_mobile, name='view_as_mobile'),

    # channel mobile
    url(r'^categorias/$', direct_to_template ,{'template':'mobile/channel_list.html'}, name='channel_list'),

    #iframe da busca
    url(r'^iframe-busca/$', direct_to_template ,{'template':'iframe/iframe.html'}, name='iframe_busca'),

    url(r'^session_items/$',session_items, name='session_items'),
    url(r'^clear_session/$',clear_session, name='clear_session'),

    # the sitemap
    #(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

