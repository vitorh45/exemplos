# coding: utf-8

from django.conf import settings
from django.core.cache import cache

def get_current_path(request):
    return {
       'current_path': "http://"+request.META.get('HTTP_HOST', '')+request.path
     }

def is_mobile(request):
    try:
        mobile = request.session['is_mobile']
        browser = request.session['view_as_browser']
    except:
        mobile = None
        browser = None
    try:
        return {'mobile': mobile, 'browser':browser}
    except:
        return {'mobile':None, 'browser':None}

