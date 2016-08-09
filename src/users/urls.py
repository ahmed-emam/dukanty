__author__ = 'mahmoud'
from django.conf.urls import patterns, url, include
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [

    # (?P<supp_name>\d+)/^$
    url(r'edit_details/$', views.edit_details),
    # url(r'sales/$', views.sales),
    # url(r'^$', views.index),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()