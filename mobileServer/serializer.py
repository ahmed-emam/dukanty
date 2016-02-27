__author__ = 'ahmedemam'
from mobileServer.models import *

from django.contrib.auth import authenticate, get_user_model
from rest_framework import exceptions, serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverShop
        #fields = ('id', 'name', 'rating', 'lat', 'lon')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverProduct
     #   fields = ('id', 'name', 'company',  'category')


# class ShopInventorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MobileserverShopinventory
#         fields = ('id', 'product', 'shop', 'stock', 'price')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverOrder
        fields = ('id', 'owner', 'shop', 'created_at', 'updated_at', 'status', 'totalprice',
                  'mobileserverorderproduct_list', 'address_list')
        #fields = ('id', 'product', 'shop', 'created_at', 'updated_at', 'status', 'totalprice')
        # fields = ('id', 'product', 'shop', 'stock', 'price')


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileserverOrderProduct

        # fields = ('id', 'product', 'shop', 'stock', 'price')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address

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




