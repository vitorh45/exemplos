#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from contact.forms import ContactForm
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, HttpResponse, Http404


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send()
            return render_to_response('contact/contact.html',
                        {'form': ContactForm()},
                        context_instance=RequestContext(request))
    else:
        form = ContactForm()
    return render_to_response('contact/contact.html',
                        {'form': form},
                        context_instance=RequestContext(request))

