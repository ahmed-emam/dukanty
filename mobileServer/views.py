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

from rest_framework import permissions, request
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import json
from django.http import HttpResponseRedirect
from django.core.exceptions import *
from django.template.loader import get_template
# Create your views here.
def index(request):
    page = render(request, "index.html", {})
    return page


"""
@apiDefine ShopNotFoundError
@apiError (NotFound) {String} ShopNotFoundError <code>shop_id</code> does not exist
@apiErrorExample {json} Error-Response:
     HTTP/1.1 500 INTERNAL SERVER ERROR
      {
        "error": "12 does not exist"
      }
"""
"""
@apiDefine ProductNotFoundError
@apiError (NotFound) {String} ProductNotFoundError <code>product_id</code> does not exist
@apiErrorExample {json} Error-Response:
     HTTP/1.1 500 INTERNAL SERVER ERROR
      {
        "error": "12 does not exist"
      }
"""
"""
@apiDefine UserNotFoundError
@apiError (NotFound) {String} UserNotFoundError user does not exist
@apiErrorExample {json} Error-Response:
     HTTP/1.1 500 INTERNAL SERVER ERROR
      {
        "error": "user does not exist"
      }
"""
"""
@apiDefine ReqParamMiss
@apiError (Incomplete) {String} RequestParamsMissing Request Missing Parameters
@apiErrorExample {json} Error-Response:
     HTTP/1.1 500 INTERNAL SERVER ERROR
      {
        "error": "Request Missing Parameters"
      }

"""
"""
@apiDefine AddressNotFoundError
@apiError (NotFound) {String} AddressNotFoundError <code>address_id</code> does not exist
@apiErrorExample {json} Error-Response:
     HTTP/1.1 500 INTERNAL SERVER ERROR
      {
        "error": "10 Missing Parameters"
      }
"""



# Render api
def api(request):
    template = get_template('doc/index.html')
   # page = render(request, "doc/index.html")
    return HttpResponse(template)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



"""
@api {get} getshops/ Get list of all shops in the system
@apiVersion 1.0.0
@apiName GetShops
@apiGroup Shop


@apiSuccess {Object[]} Shops List of all Shops

"""
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((AllowAny,))
def shops_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    print(request.user.id)
    if request.method == 'GET':
        shops = MobileserverShop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return JSONResponse(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def carts_list(request):
    carts = MobileserverCart.objects.all()
    serializer = CartSerializer(carts, many=True)
    return JSONResponse(serializer.data)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((AllowAny,))
def get_userbaskets(request):
    user = request.user
    print(user)
    baskets = MobileserverBasket.objects.filter(owner=user.id)
    serializer = BasketSerializer(baskets, many=True)
    return JSONResponse(serializer.data)



#else:

# TODO: Remove csrf_exempt
@csrf_exempt
def add_shop(request):
    print("******REQUEST*******")
    print(request.body)
    print(request.user)
    print("*********************")
    #print(request)
    # print(request.body)
    shop_name = request.POST.get('name')
    shop_rating = request.POST.get('rating')
    shop_lat = request.POST.get('lat')
    shop_lon = request.POST.get('lon')
    distance = request.POST.get('distance')
    # shop = json.loads(request.body)
    user = UsersCustomUser.objects.get(pk=1)
    print(shop_name)
    print(user)
    try:
        shop, created = MobileserverShop.objects.get_or_create\
            (name=shop_name, rating=shop_rating, lat=shop_lat, lon=shop_lon, delivery_distance=distance, owner=user)
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



# TODO: Remember in the request, you can change shop_name with shop_id and product_name with product_id


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
