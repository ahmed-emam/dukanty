__author__ = 'ahmedemam'
from mobileServer.models import *

from django.contrib.auth import authenticate, get_user_model
from rest_framework import exceptions, serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverShop
        fields = ('id', 'name', 'rating', 'lat', 'lon')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverProduct
        fields = ('id', 'name', 'company', 'price', 'img', 'category', 'tags')


class ShopInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverShopinventory
        fields = ('id', 'product', 'shop', 'stock', 'price')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverOrder
        fields = ('id', 'product', 'shop', 'stock', 'price')

class ShopProductInventory(serializers.ModelSerializer):
    class Meta:
        model = MobileserverShopproductinventory

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverCartitem

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverCart
        fields = ('id', 'checked_out', 'owner', 'cartitem_set',)

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverBasket


