from django.core.exceptions import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from mobileServer.serializer import *


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
#TODO: Remove csrf_exempt

# @api_view(['POST'])
@csrf_exempt
def create_order(request):
    print(request)

    #   Data from the POST requests
    shop_name = request.POST.get('shop_name')
    username = request.POST.get('email')
    product_name = request.POST.get('product_name')
    quantity = request.POST.get('product_quantity')
    price = request.POST.get('product_price')

    #   Check if the shop related to the order exists in my Database
    try:
        shop = MobileserverShop.objects.get(name=shop_name)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'shop wasnt found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #   Check if the customer related to the order exists in my Database
    try:
        owner = UsersCustomUser.objects.get(email=username)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'user doesnt exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #   Check if the added product exists in my Database
    try:
        product = MobileserverProduct.objects.get(name=product_name)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'product doesnt exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #   Check if the order already exists
    try:
        order = MobileserverOrder.objects.get(owner=owner, shop=shop, status=0)
        productsList = order.mobileserverorderproduct_set.all()

        #TODO: This has to impact the order linked by foreign key 'order'
        #   if the order contains a list of product
        if productsList.count() > 0:
            #  if the added-product already exists in the order, just update it
            try:
                productAddedToOrder = productsList.get(product=product)
                productAddedToOrder.quantity = quantity
                productAddedToOrder.price = price

            #  if the added-product already doesnt exist in the order, add it to the order
            except ObjectDoesNotExist:
                productAddedToOrder = MobileserverOrderProduct.objects.create\
                (order=order, product=product, quantity=int(quantity), price=float(price))
        #   if order doesn't contain any products
        # add the product to the order
        else:
            productAddedToOrder = MobileserverOrderProduct.objects.create\
                (order=order, product=product, quantity=int(quantity), price=float(price))

        productAddedToOrder.save()

        serializedData = OrderProductSerializer(productAddedToOrder)
        return JSONResponse(serializedData.data, status=status.HTTP_200_OK)
    # if the order doesn't exist
    # create it and add the product to the order
    except ObjectDoesNotExist:
        order = MobileserverOrder.objects.create(owner=owner, shop=shop)
        productAddedToOrder = MobileserverOrderProduct.objects.create\
                (order=order, product=product, quantity=int(quantity), price=float(price))
        productAddedToOrder.save()
        order.save()
        print("Created "+str(order.id))
        serializedData = OrderSerializer(order)
        return JSONResponse(serializedData.data, status=status.HTTP_200_OK)
        # print("Order doesn't exist")

@csrf_exempt
def get_orders_by_useremail(request):
    username = request.POST.get('email')
#   Check if the customer related to the order exists in my Database
    try:
        owner = UsersCustomUser.objects.get(email=username)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'user doesnt exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    orders = MobileserverOrder.objects.filter(owner=owner)
    response = []
    for order in orders:
        print(order)
        serialize_order = OrderSerializer(order)
        print(serialize_order.data)
        print(order.mobileserverorderproduct_set.all())
        serialize_order_products = OrderProductSerializer(order.mobileserverorderproduct_set.all(), many=True)
        print(serialize_order_products.data)
        response.extend({'order': serialize_order.data, 'products': serialize_order_products.data})

    print(response)
    return JSONResponse(response, status=status.HTTP_200_OK)
# def delete_order(request):

