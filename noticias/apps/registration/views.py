# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib import messages
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from registration.forms import UserCreationForm

def new(request):
    # save request.path in session
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('meuclick_index',
            args=(request.user.username,)))

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # create new user
            new_user = form.save()
            # login new user
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return HttpResponseRedirect('/meuclick/%s' % username)
        else:
            messages.add_message(request,
                messages.ERROR,
                u'Ocorreu um erro na criação da conta.'
            )
    else:
        form = UserCreationForm()
    return render_to_response('registration/new.html', {
        'form': form
        }, context_instance=RequestContext(request))


def login(request):
    # save request.path in session
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('meuclick_index',
            args=(request.user.username,)))

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # login user
            user = authenticate(username=username, password=password)
            ## check if user has request.current_site in profile.sites
            #if not user.profile.sites.filter(id=request.current_site.id):
            #    user.profile.sites.add(request.current_site)
            auth_login(request, user)
            return HttpResponseRedirect('/meuclick/%s' % username)
        else:
            messages.add_message(request,
                messages.ERROR,
                u'Ocorreu um erro no processo de login.'
            )
    else:
        form = AuthenticationForm(request)
    return render_to_response('registration/login.html', {
        'form': form
    }, context_instance=RequestContext(request))

