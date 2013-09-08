from django.conf.urls.defaults import *

urlpatterns = patterns('videos.views',
    #list all videos
    url(r'^$', 'video_list', name='video_list'),
    # videos most viewed
    url(r'^mais-vistos/$', 'most_viewed', name='videos_most_viewed'),
    #show a video
    url(r'^(?P<slug>[\w_-]+)/$', 'video_show', name='video_show'),
)

