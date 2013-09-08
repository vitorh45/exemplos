from django.conf.urls.defaults import *
from contact.views import *

#from ajax_validation.views import validate 

urlpatterns = patterns('',
    url(r'^$', contact, name='contact'),
)
