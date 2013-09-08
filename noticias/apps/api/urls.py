from django.conf.urls.defaults import *
from api.views import *

urlpatterns = patterns('',
    url(r'^news/most_viewed/$', news_list_most_viewed, name='api_news_list_most_viewed'),
    url(r'^news/latest/$', news_list_latest, name='api_news_list_latest'),
    url(r'^news/(?P<channel>[\w_-]+)/$', news_list_by_category, name='api_news_list_by_category'),
    url(r'^videos/$', video_list, name='api_video_list'),
    url(r'^blogs/$', blog_list, name='api_blog_list'),
    url(r'^blogs/(?P<blog>[\w_-]+)/$', blog_show, name='api_blog_show'),
    url(r'^clicksweek/$', clickweek_list, name='api_clickweek_list'),
    url(r'^search/', search, name='api_search'),


)

