# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.core.management.base import NoArgsCommand
from django.utils import simplejson
import urllib2
from datetime import datetime
import traceback
import sys

def cachetest():

    #verychic
    # cache key

    cache_key = 'verychic-data-%s' %  datetime.now().strftime("%d-%m-%Y")

    #if result in cache, return
    if cache.get(cache_key):
        print "if"
        return cache.get(cache_key)
    try:
        site = urllib2.urlopen('http://verychic.sodateste.com.br/last-post').read()
        data = simplejson.loads(site)
        print "try"
    except:
        return {"error":"Erro."}
    cache.set(cache_key, data, 10800)
    return data


    #faro
    #faro = urllib2.urlopen('http://faro.sodateste.com.br/last-post')
    #data = faro.read()
    #data = simplejson.loads(data)

