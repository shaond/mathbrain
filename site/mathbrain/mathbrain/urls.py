import os
import settings

from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mathbrain.views.home', name='home'),
    # url(r'^mathbrain/', include('mathbrain.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Timer App
    url(r'^examtimer/$', 'timer.views.index'),
    url(r'^exam/$', direct_to_template, {'template': 'timer.html', } ),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
            os.path.abspath(os.path.join('static/css/'))}),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
            os.path.abspath(os.path.join('static/js/'))}),
        (r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
            os.path.abspath(os.path.join('static/img/'))}),
        (r'^questions/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.abspath(os.path.join(os.curdir, '..', 'questions'))})
    )
