# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from polls.models import Poll, Choice

def poll_list(request):
    polls = Poll.objects.all()
    return render_to_response('poll_list.html', {
        'polls':polls,
    }, context_instance=RequestContext(request))

def poll_show(request, id):
    try:
        poll = Poll.objects.get(id=id,is_active=True)
    except:
        raise Http404(u'Enquete não encontrada')
    return render_to_response('poll_show.html', {
        'poll':poll,
    }, context_instance=RequestContext(request))

@csrf_exempt
def poll_vote(request, id):
    try:
        poll = Poll.objects.get(id=id)
    except:
        raise Http404(u'Enquete não encontrada.')
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()
    except:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def poll_result(request, id):
    try:
        poll = Poll.objects.get(id=id)
    except:
        raise Http404(u'Enquete não encontrada')    
    return render_to_response('poll/poll_result.html', {
        'poll':poll,
    }, context_instance=RequestContext(request))

