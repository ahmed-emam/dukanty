__author__ = 'ahmedemam'
from mobileServer.models import *

from django.contrib.auth import authenticate, get_user_model
from rest_framework import exceptions, serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'rating', 'lat', 'lon')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'company', 'price', 'img', 'category', 'tags')


class ShopInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopInventory
        fields = ('id', 'product', 'shop', 'stock', 'price')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'product', 'shop', 'stock', 'price')

class ShopProductInventory(serializers.ModelSerializer):
    class Meta:
        model = ShopProductInventory

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'checked_out', 'owner', 'cartitem_set',)

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket


