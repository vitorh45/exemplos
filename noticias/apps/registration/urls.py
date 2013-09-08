from django.conf.urls.defaults import *
#from django.contrib.auth import views as auth_views
from registration import views_from_django as auth_views

from registration import views as registration_views
from registration.forms import PasswordResetForm

urlpatterns = patterns('',

    url(r'^$', registration_views.new, name='registration_new'),

    url(r'^acessar/$', registration_views.login, name='registration_login'),

    url(r'^sair/$', auth_views.logout, {'next_page': '/'}, name='registration_logout'),

    url(r'^alterar/senha/$',
        auth_views.password_change, {'post_change_redirect' : '/'}, name='registration_password_change'),

    url(r'^alterar/senha/ok/$', auth_views.password_change_done,
        name='registration_password_change_done'),

    url(r'^recuperar/senha/$',
        auth_views.password_reset, {'password_reset_form' : PasswordResetForm},
        name='registration_password_reset'),

    url(r'^recuperar/senha/confirmar/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='registration_password_reset_confirm'),

    url(r'^recuperar/senha/completar/$',
        auth_views.password_reset_complete,
        name='registration_password_reset_complete'),

    url(r'^recuperar/senha/ok/$', auth_views.password_reset_done,
        name='registration_password_reset_done'),



)

