__author__ = 'ahmedemam'
from django.conf.urls import patterns, url, include
from django.conf import settings
from . import views, orderUtils, inventoryUtils, pushNotifications, productUtils
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'getshops/$', views.shops_list),
    url(r'getproducts/$', productUtils.products_list),
    url(r'getcarts/$', views.carts_list),
    url(r'getbaskets/$', views.get_userbaskets),
    url(r'getshopinventory/$', inventoryUtils.get_shopInventory),
    url(r'addimage/$', productUtils.add_image),
    url(r'getimage/(?P<image_id>\d+)/$', productUtils.getImage),
    # DEBUGGING routes
    url(r'debug/addshop/', views.add_shop),
    url(r'debug/addproduct/', productUtils.add_product),
    url(r'debug/inventory/', inventoryUtils.create_inventory),
    url(r'debug/createorder/', orderUtils.create_order),
    url(r'debug/getordersbyemail/', orderUtils.get_orders_by_useremail),
    # DEBUGGING routes

    url(r'registerAndroidDevice/$', pushNotifications.registerAndroidDevice),

    url(r'^$', views.index),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
