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
from django.core.exceptions import *
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

'''
if order exists:
    -if product exists
        update quantity and price
    -if product doesnt exist
        add product
if order doesnt exist
    -create order
    -add product


TODO:
    check status of order
'''
#TODO: Write this in a cleaner way
# @api_view(['POST'])
def create_order(request):
    print(request)

    shop_name = request.POST.get('shop_name')
    username = request.POST.get('email')

    try:
        shop = MobileserverShop.objects.get(name=shop_name)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'shop wasnt found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        owner = UsersCustomUser.objects.get(email=username)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'user doesnt exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    product_name = request.POST.get('product_name')
    quantity = request.POST.get('product_quantity')
    price = request.POST.get('product_price')
    try:
        product = MobileserverProduct.objects.get(name=product_name)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'product doesnt exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        order = MobileserverOrder.objects.get(owner=owner, shop=shop, status=0)
        productsList = order.mobileserverorderproduct_set.all()


        #TODO: This has to impact the order linked by foreign key 'order'
        if productsList.count() > 0:
            try:
                productAddedToOrder = productsList.get(product=product_name)
                productAddedToOrder.quantity = quantity
                productAddedToOrder.price = price

            except ObjectDoesNotExist:
                productAddedToOrder = MobileserverOrderProduct.objects.create\
                (order=order, product=product, quantity=int(quantity), price=float(price))

        else:
            productAddedToOrder = MobileserverOrderProduct.objects.create\
                (order=order, product=product, quantity=int(quantity), price=float(price))

        productAddedToOrder.save()

        serializedData = OrderProductSerializer(productAddedToOrder)
        return JSONResponse(serializedData.data, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        order = MobileserverOrder.objects.create(owner=owner, shop=shop)


        productAddedToOrder = MobileserverOrderProduct.objects.create\
                (order=order, product=product, quantity=int(quantity), price=float(price))
        productAddedToOrder.save()
        order.save()
        print("Created "+order.id)
        serializedData = OrderSerializer(order)
        return JSONResponse(serializedData.data, status=status.HTTP_200_OK)
        # print("Order doesn't exist")


# def delete_order(request):

