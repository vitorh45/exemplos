# -*- coding: utf-8 -*-
from django.core.cache import cache

import urllib2
import re
from datetime import datetime, timedelta, date

class Mares:

    def getMares(self):
        hoje = datetime.now().strftime("%d/%m/%Y")
        amanha = datetime.now() + timedelta(days=1)
        amanha = amanha.strftime("%d/%m/%Y")
        string_mes = self.string_month(str(datetime.now().month))
        ano = datetime.now().year

        # cache key
        cache_key = 'mares-%s' %  datetime.now().strftime("%d-%m-%Y")
        # if result in cache, return
        if cache.get(cache_key):
            return cache.get(cache_key)
        try:
            site = urllib2.urlopen('http://www.mar.mil.br/dhn/chm/tabuas/30540%s%s.htm' % (string_mes, ano)).readlines()
            mares = []
            horarios = []
            for linha in site:
                if linha.find(hoje) > 0 :
                    index = site.index(linha)
                    for i in range(1,30):
                        if site[index+i].find(amanha) > 0 :
                            break
                        elif site[index+i].find("BGCOLOR") > 0:
                            er1 = re.findall(r'[0-9]{1,2}\:[0-9]{1,2}',site[index+i])
                            er2 = re.findall(r'[0-9]{1,2}\.[0-9]{1,2}',site[index+i])
                            if len(er1) > 0:
                                horarios.append(er1[0])
                            if len(er2) > 0:
                                mares.append(er2[0])
            lista_mares = []
            for i in range(len(horarios)):
                hora = datetime.strptime(horarios[i],"%H:%M")
                lista_mares.append((hora,float(mares[i])))
            output = {'status':'ok','values':lista_mares}
            cache.set(cache_key, output, 3600 * 12)
            return output
        except:
            #response = {'status':'error','message':'u'Serviço indisponível no momento.'}
            return {'status':'error','message':u'Serviço indisponível no momento.'}

    def string_month(self,month):
        mes = None
        if month == "1":
            mes = "Jan"
        if month == "2":
            mes = "Fev"
        if month == "3":
            mes = "Mar"
        if month == "4":
            mes = "Abr"
        if month == "5":
            mes = "Mai"
        if month == "6":
            mes = "Jun"
        if month == "7":
            mes = "Jul"
        if month == "8":
            mes = "Ago"
        if month == "9":
            mes = "Set"
        if month == "10":
            mes = "Out"
        if month == "11":
            mes = "Nov"
        if month == "12":
            mes = "Dez"
        return mes

