from django.shortcuts import render
from rest_framework import viewsets
from mobileServer.models import *
from mobileServer.serializer import *
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, permissions, status, response, views
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import json

# Create your views here.
def index(request):
    page = render(request, "index.html", {})
    return page

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def shops_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        shops = MobileserverShop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return JSONResponse(serializer.data)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def products_list(request):
    if request.method == 'GET':
        products = MobileserverProduct.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JSONResponse(serializer.data)
    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = SnippetSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JSONResponse(serializer.data, status=201)
    #     return JSONResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def carts_list(request):
    carts = MobileserverCart.objects.all()
    serializer = CartSerializer(carts, many=True)
    return JSONResponse(serializer.data)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_userbaskets(request):
    user = request.user
    print(user)
    baskets = MobileserverBasket.objects.filter(owner=user.id)
    serializer = BasketSerializer(baskets, many=True)
    return JSONResponse(serializer.data)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_shopInventory(request):
    shop_id = request['shop_id']
    # Get the shop using shop ID
    shop = MobileserverShop.objects.get(pk=shop_id)
    # if the shop exists
    if shop:
        # Get all inventory entries that are linked to that shop
        inventory = MobileserverShopproductinventory.objects.filter(shop=shop)
        # Response sent back to the user
        response = []
        # loop over all the inventory entries found
        for inventoryEntry in inventory:
            related_product = inventoryEntry.product
            productSerialized = ProductSerializer(related_product)
            response.extend([{
                "product": productSerialized,
                "price": inventoryEntry.price,
                "stock": inventoryEntry.stock
            }])

        return JSONResponse(response)


#else:
        #TODO: Return an error

@csrf_exempt
def add_shop(request):
    print(request.body)
    shop = json.load(request.body)
    print(shop)
    return Response(status=status.HTTP_200_OK)

# def getshops(request):
#     return

#
# @api_view(['GET'])
# @api_view(['GET'])
# ViewSets define the view behavior.
# class ShopViewSet(viewsets.ModelViewSet):
#     queryset = Shop.objects.all()
#     serializer_class = ShopSerializer
