from django.conf.urls.defaults import *

urlpatterns = patterns('polls.views',
    #url(r'^$', 'poll_list', name='poll_list'),
    #url(r'^(?P<id>[\w_-]+)/$', 'poll_show', name='poll_show'),
    url(r'^(?P<id>[\w_-]+)/votar$', 'poll_vote', name='poll_vote'),
    url(r'^(?P<id>[\w_-]+)/resultado$', 'poll_result', name='poll_result'),
)

