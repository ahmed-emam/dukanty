from django.core.exceptions import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
import json
from mobileServer.serializer import *
from mobileServer.user_utils import add_address


#Order Status
NOT_ORDERED = 0
ORDER_ISSUED = 1
ORDER_ON_DELIVERY = 2
ORDER_DELIVERED = 3

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
'''
Function that will create/update order

POST request
shop_name:  <Related shop name>
email:   <user's email, the user making the order>
product_name: <Product to be added to the order>
product_price:  <Price of product in the shop, this will be multiplied by the quantity>
product_quantity:  <Ordered quantity of the product>
'''
#@api_view(['POST'])
@csrf_exempt
def create_order(request):
    print("******REQUEST*******")
    print(request.META)
    print(request.POST)
   # print(request.query_params)
    print(request.user)
    print("*********************")

    #   Data from the POST requests

    if 'shop_id' not in request.POST or 'user_id' not in request.POST or 'product_list' not in request.POST\
            or 'mobile' not in request.POST or 'name' not in request.POST:
        return JSONResponse({'error': 'request is missing parameters'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if 'address_id' not in request.POST:
        #add address
        print "Address does not exist"
    else:
        address_id = request.POST.get('address_id')

    shop_id = request.POST.get('shop_id')
    username = request.POST.get('user_id')
    product_list = request.POST.get('product_list')
    mobile = request.POST.get('mobile')
    name = request.POST.get('name')

    print(shop_id+" "+username+" "+product_list)

    product_list = json.loads(product_list)

        #print product
    #   Check if the shop related to the order exists in my Database
    try:
        shop = MobileserverShop.objects.get(pk=int(shop_id))
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'shop wasnt found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #   Check if the customer related to the order exists in my Database
    try:
        owner = UsersCustomUser.objects.get(pk=int(username))
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'user doesnt exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #   Check if the added product exists in my Database

    #   Check if the order already exists
    # try:
    #     order = MobileserverOrder.objects.get(owner=owner, shop=shop, status=0)
    #
    #     # order has not been checkout
    #     if order.status < 1:
    #         productsList = order.mobileserverorderproduct_set.all()
    #
    #         #TODO: This has to impact the order linked by foreign key 'order'
    #         #   if the order contains a list of product
    #         if productsList.count() > 0:
    #             #  if the added-product already exists in the order, just update it
    #             try:
    #                 productAddedToOrder = productsList.get(product=product)
    #                 productAddedToOrder.quantity = quantity
    #                 productAddedToOrder.price = price
    #
    #             #  if the added-product already doesnt exist in the order, add it to the order
    #             except ObjectDoesNotExist:
    #                 productAddedToOrder = MobileserverOrderProduct.objects.create\
    #                 (order=order, product=product, quantity=int(quantity), price=float(price))
    #         #   if order doesn't contain any products
    #         # add the product to the order
    #         else:
    #             productAddedToOrder = MobileserverOrderProduct.objects.create\
    #                 (order=order, product=product, quantity=int(quantity), price=float(price))
    #
    #         productAddedToOrder.save()
    #
    #         serializedData = OrderProductSerializer(productAddedToOrder)
    #         return JSONResponse(serializedData.data, status=status.HTTP_200_OK)
    #     else:
    #         print("Changing order failed for\n"+order.__str__())
    # # if the order doesn't exist
    # # create it and add the product to the order
    # except ObjectDoesNotExist:
    order = MobileserverOrder.objects.create(owner=owner, shop=shop, name=name, mobile=mobile)

    for product in product_list:
        product_name = product['product_name']
        product_price = product['product_price']
        product_quantity = product['product_quantity']
        try:
            product = MobileserverProduct.objects.get(name=product_name)
        except ObjectDoesNotExist:
            order.delete()
            return JSONResponse({'error': str(product_name)+' doesnt exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        productAddedToOrder = MobileserverOrderProduct.objects.create\
                (order=order, product=product, quantity=int(product_quantity), price=float(product_price))
        productAddedToOrder.save()

    #returned = add_address(request, order)
    #print (returned)
    change_order_status(order, ORDER_ISSUED)
    order.save()

    print("Created order id:"+str(order.id))
    serializedData = OrderSerializer(order)
    print serializedData.data
    return JSONResponse(serializedData.data, status=status.HTTP_200_OK)
        # print("Order doesn't exist")

'''
Function will get all the orders linked to the user with the email given as a POST request parameter

POST request

email:  <User's email>

'''
@csrf_exempt
def get_orders_by_useremail(request):
    username = request.POST.get('user_email')
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
        response.extend([{'order': serialize_order.data, 'products': serialize_order_products.data}])
    print(response)
    response = json.dumps(response , separators=(',' , ':'))
    print(response)
    return JSONResponse(response, status=status.HTTP_200_OK)


def change_order_status(order, status):
    print("change status of order "+order+" from "+str(order.status)+" -> "+str(status))
    order.status = status
    order.save()


def checkout_order(request):
    print("******REQUEST*******")
    print(request.body)
  #  print(request.query_params)
    print(request.user)
    print("*********************")

    order_id = request.POST.get('order_id')

    try:
        order = MobileserverOrder.objects.get(pk=order_id)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'order doesnt exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    change_order_status(order, ORDER_ISSUED)
    return JSONResponse({'success': 'order has been changed'}, status=status.HTTP_200_OK)


def deliver_order(request):
    print("******REQUEST*******")
    print(request.body)

    print(request.user)
    print("*********************")

    order_id = request.POST.get('order_id')

    try:
        order = MobileserverOrder.objects.get(pk=order_id)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'order doesnt exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    change_order_status(order, ORDER_ON_DELIVERY)
    return JSONResponse({'success': 'order has been changed'}, status=status.HTTP_200_OK)
# def delete_order(request):

