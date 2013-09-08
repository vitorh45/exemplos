# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.defaultfilters import slugify
from datetime import datetime
from meuclick.models import UserMeuClick
from registration.utils import EmailThread
from common.tasks import celery_send_email
import random, hashlib
import traceback, sys

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    name = forms.CharField(label='Nome completo',max_length=120)
    #username = forms.RegexField(label=u"Login", max_length=30, regex=r'^[\w.+-]+$',
    #    help_text = u"30 caracteres ou menos. Letras e números apenas, não é permitido uso de letras maiúsculas.",
    #    error_messages = {'invalid': u"Esse valor só deve conter letras e números, não é permitido uso de letras maiúsculas."})
    password1 = forms.CharField(label=u"Senha", help_text = u'A senha deve conter seis caracteres ou mais.', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u"Confirmar senha", widget=forms.PasswordInput,
        help_text = u"Entre com a mesma senha, para verificação.")

    class Meta:
        model = User
        fields = ("username","email")
        exclude = ("username")
    '''
    def clean_username(self):
        username = self.cleaned_data["username"]
        username_lower = self.cleaned_data["username"].lower()
        if username != username_lower:
            raise forms.ValidationError(u"O nome de usuário não deve conter letras maiúsculas.")
        #if username in settings.BANNED_USERNAMES:
        #    raise forms.ValidationError(u"Nome de usuário indisponível.")
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(u"Um usuário com esse nome já existe.")
        except User.DoesNotExist:
            return username
    '''
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        if len(password1) < 6:
            raise forms.ValidationError("A senha deve conter seis caracteres ou mais.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if len(password2) < 6:
            raise forms.ValidationError("A senha deve conter seis caracteres ou mais.")
        if password1 != password2:
            raise forms.ValidationError("As duas senhas não conferem.")
        return password2

    def clean_email(self):
        if len(self.cleaned_data['email']) == 0:
            raise forms.ValidationError(u"Este campo é obrigatório.")
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(u"Esse e-mail já está em uso. Por favor escolha outro.")
        return self.cleaned_data['email']

    def save(self, commit=True, invite_token=None, site=None):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        # save zipcode in userprofile
        user_profile, created = UserMeuClick.objects.get_or_create(
                    user=user)
        user_profile.name = self.cleaned_data["name"]
        user_profile.creation_date = datetime.now()
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        token = hashlib.sha1(salt+user.username).hexdigest()
        user_profile.token = token
        user_profile.save()

        # sending the email activation
        domain = Site.objects.get_current().domain
        titulo = u"ClickPB - email de ativação de cadastro"
        destino = (user.email,)
        texto = u"Clique no link abaixo para a ativação do seu cadastro no ClickPB\n"
        if not domain.startswith("http://"):
            domain = "http://"+domain
        if not domain.endswith("/"):
            domain = domain + "/"
        texto += u"%svcnoclick/cadastro/ativacao/%s" % (domain,token)

        celery_send_email.apply_async(args=[titulo, texto, "naoresponda@clickpb.com.br",destino], priority=0)
        #EmailThread(titulo, texto, "dotamirana@hotmail.com",destino).start()
        #send_mail(subject=titulo,message=texto,from_email="",recipient_list=destino,)
        # return user
        return user


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = forms.EmailField(label=_("Email"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError(u"Email ou senha inválidos")

        try:
            user = UserMeuClick.objects.get(user__email=email)
        except:
            raise forms.ValidationError(u"Email ou senha inválidos")

        if not user.is_active:
            raise forms.ValidationError(u"Esse email pertence a um cadastro não ativado.")

        return self.cleaned_data


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=75)

    def clean_email(self):
        """
        Validates that a user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        user = User.objects.filter(email__iexact=email)
        if len(user) == 0:
            raise forms.ValidationError("Esse email não está associado a nenhuma conta. Verifique.")
        return email

    def send_email_(self):
        # sending the email activation
        email = self.cleaned_data["email"]
        try:
            user = UserMeuClick.objects.get(user__email=email)
            token = user.token
        except:
            raise Http404()
        domain = Site.objects.get_current().domain
        titulo = u"ClickPB - email de reset da senha"
        destino = [email]
        texto = u"Clique no link abaixo para alterar sua senha no ClickPB\n"

        if not domain.startswith("http://"):
            domain = "http://"+domain
        if not domain.endswith("/"):
            domain = domain + "/"

        texto += u"%svcnoclick/cadastro/resetar-senha/%s" % (domain,token)

        #EmailThread(titulo, texto, "",destino).start()
        celery_send_email.apply_async(args=[titulo, texto, "naoresponda@clickpb.com.br",destino], priority=0)
        #send_mail(subject=titulo,message=texto,from_email="",recipient_list=destino,)

class NewPasswordForm(forms.Form):
    password1 = forms.CharField(label=u"Senha", help_text = u'A senha deve conter seis caracteres ou mais.', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u"Confirmar senha", widget=forms.PasswordInput,
        help_text = u"Entre com a mesma senha, para verificação.")

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        if len(password1) < 6:
            raise forms.ValidationError("A senha deve conter seis caracteres ou mais.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if len(password2) < 6:
            raise forms.ValidationError("A senha deve conter seis caracteres ou mais.")
        if password1 != password2:
            raise forms.ValidationError("As duas senhas não conferem.")
        return password2

