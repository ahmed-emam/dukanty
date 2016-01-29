from django.shortcuts import render
from rest_framework import viewsets
from mobileServer.models import *
from users.models import  *
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

from django.core.exceptions import *

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


# TODO: Rewrite code for get_shopInventory function using exceptions
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

# TODO: Remove csrf_exempt
@csrf_exempt
def add_shop(request):
    print(request)
    # print(request.body)
    shop_name = request.POST.get('name')
    shop_rating = request.POST.get('rating')
    shop_lat = request.POST.get('lat')
    shop_lon = request.POST.get('lon')
    # shop = json.loads(request.body)
    print(shop_name)
    try:
        shop, created = MobileserverShop.objects.get_or_create\
            (name=shop_name, rating=shop_rating, lat=shop_lat, lon=shop_lon)
        shop.save()
        serializedData = ShopSerializer(shop)
        return JSONResponse(serializedData.data, status=status.HTTP_200_OK)
    except MultipleObjectsReturned:
        return JSONResponse({'error': 'Found multiple entries'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # if shop.id:
    #     print("Added shop id "+str(shop.id))
    #     return JSONResponse({'added': shop_name}, status=status.HTTP_200_OK)
    # else:
    #     print("Didnt add "+shop_name)
    #     return JSONResponse({'error': 'couldnt add'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def add_product(request):
    print(request)
    # print(request.body)
    product_name = request.POST.get('name')
    product_company = request.POST.get('company')
    product_category = request.POST.get('category')
    product_img = request.POST.get('img')
    # shop = json.loads(request.body)
    print(product_name)
    product = MobileserverProduct.objects.create\
        (name=product_name, company=product_company, category=product_category, img=product_img)
    product.save()
    if product.id:
        print("Added shop id "+str(product.id))
        return JSONResponse({'added': product_name}, status=status.HTTP_200_OK)
    else:
        print("Didnt add "+product_name)
        return JSONResponse({'error': 'couldnt add'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# TODO: Remember in the request, you can change shop_name with shop_id and product_name with product_id
'''

Function that will create/update inventory of a shop
Inventory is a list of products
List is linked to a shop, owner of the shop(he is the only one who can edit the list)
For each product in the list we have a price customized by the shop, and the option of whether its in stock or not

POST request
shop_name:  <Related shop name>
product_name:   <Product to be added to inventory>
owner_name: <Owner of the shop>
price:  <Price of product in the shop>
stock:  <In Stock/Out of Stock>

'''
#TODO: Remove csrf_exempt
@csrf_exempt
def create_inventory(request):
    print(request)

    shop_name = request.POST.get('shop_name')
    try:
        shop = MobileserverShop.objects.get(name=shop_name)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'shop wasnt found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    owner = UsersCustomUser.objects.get(pk=1)

    product_name = request.POST.get('product_name')
    try:
        product = MobileserverProduct.objects.get(name=product_name)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'product wasnt found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    price = request.POST.get('price')
    stock = request.POST.get('stock')
    if stock=="False":
        stock = False
    else:
        stock = True

    print(price)
    print(stock)
    try:
        inventory_entry, created = MobileserverShopproductinventory.objects.get_or_create(shop=shop, product=product, owner=owner)
        print(inventory_entry)
        inventory_entry.price = float(price)
        inventory_entry.stock = stock
        inventory_entry.save()
        serializedData = ShopProductInventory(inventory_entry)
        return JSONResponse(serializedData.data, status=status.HTTP_200_OK)
    except MultipleObjectsReturned:
        return JSONResponse({'error': 'Found multiple entries'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    # if inventory_entry is None:
    #     inventory_entry = MobileserverShopproductinventory.objects.create\
    #         (price=price, stock=stock, product=product, owner=owner, shop=shop)
    #     inventory_entry.save()
    #     return JSONResponse(json.dumps(inventory_entry), status=status.HTTP_200_OK)
    # else:

# def getshops(request):
#     return

#
# @api_view(['GET'])
# @api_view(['GET'])
# ViewSets define the view behavior.
# class ShopViewSet(viewsets.ModelViewSet):
#     queryset = Shop.objects.all()
#     serializer_class = ShopSerializer
