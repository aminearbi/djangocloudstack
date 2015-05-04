"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm
from app.views import *

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^createvm','app.views.createvm',name='createvm'),
    url(r'^template$', 'app.views.template', name='template'),
    url(r'^about', 'app.views.about', name='about'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    url(r'^hello/$', hello),
   # url(r'^current/$', current),
    url(r'^port/$', SetPortforwarding,name='port'),
    url(r'^portSuccess/$', CreatePortForwardingRule),
    url(r'^stopvm/$', stopvm,name='stop'),
    url(r'^listvms/$', listvm,name='listvm'),
    url(r'^stopvmresult/$', stopvmresult),
    url(r'^startvm/$', startvm,name='start'),
    url(r'^startvmresult/$', startvmresult),
    url(r'^destroyvm/$', destroyvm,name='destroy'),
    url(r'^destroyvmresult/$', destroyvmresult),
    url(r'^chat/$', chat,name='chat'),
    url(r'^chatlive/$', chatlive),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
