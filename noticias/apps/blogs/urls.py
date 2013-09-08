from django.conf.urls.defaults import *

urlpatterns = patterns('blogs.views',
    #list all the blogs
    url(r'^$', 'blog_list', name='blog_list'),
    url(r'^ultimas-postagens/$', 'latest', name='posts_latest'),
    url(r'^postagens-mais-lidas/$', 'most_viewed', name='posts_most_viewed'),
    url(r'^comentarios/incrementar/(?P<slug>[\w_-]+)/$', 'increment_comments',name='increment_comments_post'),    url(r'^comentarios/decrementar/(?P<slug>[\w_-]+)/$', 'decrement_comments',name='decrement_comments_post'),
    #list all the posts of a blog
    url(r'^(?P<blog>[\w_-]+)/$', 'blog_show', name='blog_show'),
    #list all the posts of a blog per year
    url(r'^(?P<blog>[\w_-]+)/(?P<year>[0-9]{4})/$', 'blog_show_by_year', name='blog_show_by_year'),
    #list all the posts of a blog per month from 2011
    url(r'^(?P<blog>[\w_-]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', 'blog_show_by_month', name='blog_show_by_month'),
    #show the print page of a post
    url(r'^(?P<blog>[\w_-]+)/(?P<slug>[\w_-]+)/imprimir/$', 'post_print', name='post_print'),
    #show the detail of a post
    url(r'^(?P<blog>[\w_-]+)/(?P<slug>[\w_-]+)/$', 'post_show', name='post_show'),
)

