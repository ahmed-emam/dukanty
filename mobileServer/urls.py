__author__ = 'ahmedemam'
from django.conf.urls import patterns, url, include
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'getshops/$', views.shops_list),
    url(r'getproducts/$', views.products_list),
    url(r'getcarts/$', views.carts_list),
    url(r'getbaskets/$', views.get_userbaskets),
    url(r'^$', views.index),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
