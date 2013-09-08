# -*- coding: utf-8 -*-
from django.core.cache import cache

import urllib2
import re
from datetime import datetime

def getQuotation():
    # cache key
    cache_key = 'dolar-data-%s' %  datetime.now().strftime("%d-%m-%Y")
    #if result in cache, return
    if cache.get(cache_key):
        return cache.get(cache_key)
    try:
        site = urllib2.urlopen('http://economia.uol.com.br/cotacoes/').readlines()
    except:
        return {'status':'error','message':u'Serviço indisponível no momento.'}
    dolar = []
    euro = []
    bovespa = None
    nasdaq = None
    variacao_euro = None
    variacao_dolar = None
    last_update_bolsa = None
    last_update_moeda = None
    cont = 0
    for linha in site:
        if linha.find("Euro") > 0 and linha.find("em R$") > 0:
            euro = re.findall(r'[+-]?[0-9]+\,[0-9]+%?',linha)

        if linha.find('comercial <span class="compl"') > 0 and linha.find("R$") > 0:
            dolar = re.findall(r'[+-]?[0-9]+(?:\,[0-9]+)%?',linha)

        if linha.find("Brasil") > 0 and linha.find("Bovespa") > 0:
            bovespa = re.findall(r'[-+]?[0-9]+(?:\,[0-9]+)?%',linha)

        if linha.find("EUA") > 0 and linha.find("Nasdaq") > 0 and linha.find("variacao") > 0:
            nasdaq = re.findall(r'[-+]?[0-9]+(?:\,[0-9]+)?%',linha)

        if linha.find('p class="data-hora"') > 0:
            #if "Brasil" not in line and "Bovespa" not in line and "Global 40" not in line:
            if cont == 0:
                last_update_bolsa = re.findall(r'[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s*[0-9]{1,2}:[0-9]{2}',linha)[0]
            cont+=1

    try:
        eurocompra = euro[0].replace(',','.')
        eurocompra = round(float(eurocompra),2)
        eurocompra = str(eurocompra).replace('.',',')
    except:
        eurocompra = "-"

    try:
        eurovenda = euro[1].replace(',','.')
        eurovenda = round(float(eurovenda),2)
        eurovenda = str(eurovenda).replace('.',',')
    except:
        eurovenda = "-"

    try:
        eurovariacao = euro[2][:-1].replace(',','.')
        eurovariacao = round(float(eurovariacao),2)
        eurovariacao = str(eurovariacao).replace('.',',')
    except:
        eurovariacao = "-"

    try:
        dolarcompra = dolar[0].replace(',','.')
        dolarcompra = round(float(dolarcompra),2)
        dolarcompra = str(dolarcompra).replace('.',',')
    except:
        dolarcompra = "-"

    try:
        dolarvenda = dolar[1].replace(',','.')
        dolarvenda = round(float(dolarvenda),2)
        dolarvenda = str(dolarvenda).replace('.',',')
    except:
        dolarvenda = "-"

    try:
        dolarvariacao = dolar[2][:-1].replace(',','.')
        dolarvariacao = round(float(dolarvariacao),2)
        dolarvariacao = str(dolarvariacao).replace('.',',')
    except:
        dolarvariacao = "-"

    try:
        bovespa = bovespa[0]
        nasdaq = nasdaq[0]
        dados = {'status': 'ok','eurocompra':eurocompra,'eurovenda':eurovenda,'eurovariacao':eurovariacao,
        'dolarcompra':dolarcompra,'dolarvenda':dolarvenda,'dolarvariacao':dolarvariacao,
        'bovespa':bovespa,'nasdaq':nasdaq, 'last_update_bolsa':last_update_bolsa}
        # set value in cache
        cache.set(cache_key, dados, 3600)
        return dados
    except:
        return None

