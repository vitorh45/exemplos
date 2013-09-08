# -*- coding: utf-8 -*-

from django import forms
from django.core.mail import send_mail
from django.conf import settings
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(label=u'Nome')
    email = forms.EmailField(label=u'E-mail', required=True)
    subject = forms.CharField(label='Assunto')
    message = forms.Field(label=u'Mensagem', widget=forms.Textarea)
    captcha = CaptchaField()

    def send(self):
        titulo = '[CLICKPB - CONTATO]'
        destino = settings.EMAILS
        fromemail = self.cleaned_data["email"]
        #destino = (("vitorh45@gmail.com"),("huayna@gmail.com"))

        texto = """
        Nome: %(name)s
        E-mail: %(email)s
        Assunto: %(subject)s
        Mensagem:
        %(message)s
        """ % self.cleaned_data

        send_mail(
        subject=titulo,
        message=texto,
        from_email=fromemail,
        recipient_list=destino,
     )

