# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from apps.videos.models import Video
from comments.forms import CommentForm
from datetime import datetime

def video_list(request):
    videos = Video.objects.all()
    page = request.GET.get('page','1')
    return render_to_response('videos/video_list.html', {
        'videos': videos,
        'page':page,
    }, context_instance=RequestContext(request))

def video_show(request, slug):
    try:
        video = Video.objects.get(slug=slug)
    except:
        raise Http404(u'Vídeo não encontrado.')

    related_videos = video.get_related_videos()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.submit_date = datetime.now()
            comment.user = None
            comment.site = Site.objects.get_current()
            comment.ip_address = request.META.get("REMOTE_ADDR", None)
            comment.content_type = ContentType.objects.get_for_model(video)
            comment.object_pk = video.id
            comment.save()
            return HttpResponseRedirect(reverse('video_show',args=[video.slug]))
    else:
        form = CommentForm()

    return render_to_response('videos/video_show.html', {
        'video': video,
        'related_videos':related_videos,
        'form':form,
    }, context_instance=RequestContext(request))

def most_viewed(request):
    videos = Video.objects.order_by('-views_count')
    page = request.GET.get('page','1')
    return render_to_response('videos/video_most_viewed.html', {
        'videos': videos,
        'page':page,
    }, context_instance=RequestContext(request))

