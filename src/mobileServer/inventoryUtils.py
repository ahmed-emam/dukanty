from django.core.exceptions import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from serializer import *
from models import *
from error import *


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


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
"""
@api {post} debug/inventory/ create/update Shop Inventory
@apiVersion 1.0.0
@apiName CreateShopInventory
@apiGroup Shop
@apiParam {Number} shop_id Shop unique ID.
@apiParam {Number} product_id Product to be created/updated unique ID.
@apiParam {Number} price Product's price
@apiParam {Number} stock    Product stock level

@apiSuccess {Object} product created/updated product serialized data

@apiUse ShopNotFoundError
@apiUse ProductNotFoundError
"""
#TODO: Remove csrf_exempt
#TODO: Accept list of products
@csrf_exempt
def create_inventory(request):
    print("******REQUEST*******")
    print(request.body)
  #  print(request.query_params)
    print(request.user)
    print("*********************")

    #shop_name = request.POST.get('shop_name')
    shop_id = request.POST.get('shop_id')
    try:
        #shop = MobileserverShop.objects.get(name=shop_name)
    	shop = MobileserverShop.objects.get(id=shop_id)
    except ObjectDoesNotExist:
        return JSONResponse({'error': ShopNotFound}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    owner = UsersCustomUser.objects.get(pk=1)


    product_id = request.POST.get('product_id')
    try:
        product = MobileserverProduct.objects.get(id=product_id)
    except ObjectDoesNotExist:
        return JSONResponse({'error': ProductNotFound}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    price = request.POST.get('price')
    stock = request.POST.get('stock')


    print(price)
    print(stock)
    try:
        inventory_entry, created = MobileserverShopproductinventory.objects.get_or_create(shop=shop, product=product)
        print(inventory_entry)
        inventory_entry.price = float(price)
        inventory_entry.stock = int(stock)
        inventory_entry.save()
        serializedData = ShopProductInventory(inventory_entry)
        return JSONResponse(serializedData.data, status=status.HTTP_200_OK)
    except MultipleObjectsReturned:
        return JSONResponse({'error': 'Found multiple entries'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
@api {GET} inventory/get_shop/:shop_id Get Shop Inventory
@apiVersion 1.0.0
@apiName GetShopInventory
@apiGroup Shop
@apiParam {Number} shop_id Shop unique ID.
@apiSuccess {Object} product Product serialized data
@apiSuccess {Number} price Product's price
@apiSuccess {Boolean} Stock Product in Stock/out of stock
@apiSuccess {Number} image_width Product's image width
@apiSuccess {Number} image_height Product's image height

@apiUse ShopNotFoundError
"""


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_shopInventory(request, shop_id):
    print("******REQUEST*******")
    print(request.body)
    print(request.user)
    print("*********************")

    # shop_id = request.GET.get('shop_id')
    shop_id = shop_id

    print(shop_id)
    # Get the shop using shop ID
    try:
        shop = MobileserverShop.objects.get(pk=shop_id)

    except ObjectDoesNotExist:
        return JSONResponse({'Error': ShopNotFound}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Get all inventory entries that are linked to that shop
    inventory = MobileserverShopproductinventory.objects.filter(shop=shop)
    # Response sent back to the user
    response = []
    # loop over all the inventory entries found
    for inventoryEntry in inventory:
        related_product = inventoryEntry.product
        imageObject = Image.objects.get(product=related_product.id)
        productSerialized = ProductSerializer(related_product)
        # why are you extending here?
        response.extend([{
            "product": productSerialized.data,
            "price": inventoryEntry.price,
            "stock": inventoryEntry.stock,
            "image_width": imageObject.image.width,
            "image_height": imageObject.image.height,
        }])

    return JSONResponse(response)


"""
@api {POST} /inventory/check_in Check in products 
@apiVersion 1.0.0
@apiName check_in
@apiGroup Shop
The ones below are incorrect, will come back to them in a moment
@apiSuccess {Object} product Product serialized data
@apiSuccess {Number} price Product's price
@apiSuccess {Boolean} Stock Product in Stock/out of stock
@apiSuccess {Number} image_width Product's image width
@apiSuccess {Number} image_height Product's image height

@apiUse ShopNotFoundError
"""


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def check_in(request):
    user = request.user
    # check user is authenticated
    # check user is owner/superuser

    # tying/catching does not always work because you will get none
    try:
        shop_id = request.data['shop_id']
        products_list = request.data['products_list']
    except KeyError:
        return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # got the parameters, lets check them in
    # assumes that shop and all products already exist
    for product in products_list:
        # product = {'id': 50, 'quantity': 10}
        # line below might not work, needs to be tested
        try:
            shop_db = MobileserverShop.objects.get(pk=shop_id)
            product_db = MobileserverProduct.objects.get(id=product['id'])
            inventory_product = MobileserverShopproductinventory.objects.get(shop=shop_db, product=product_db)
        except ObjectDoesNotExist:
            return JSONResponse({'error': 'Either shop or product do not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print "Current stock", inventory_product.stock
        inventory_product.stock += product['quantity']
        # timestamp will be updated on save
        inventory_product.save()

    # need to change the type of the response
    return JSONResponse({'success'})


"""
@api {POST} /inventory/check_out Check out products 
@apiVersion 1.0.0
@apiName check_out
@apiGroup Shop
The ones below are incorrect, will come back to them in a moment
@apiSuccess {Object} product Product serialized data
@apiSuccess {Number} price Product's price
@apiSuccess {Boolean} Stock Product in Stock/out of stock
@apiSuccess {Number} image_width Product's image width
@apiSuccess {Number} image_height Product's image height

@apiUse ShopNotFoundError
"""
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def check_out(request):
    user = request.user
    # check user is authenticated
    # check user is owner/superuser

    # tying/catching does not always work because you will get none
    try:
        shop_id = request.data['shop_id']
        products_list = request.data['products_list']
    except KeyError:
        return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # got the parameters, lets check them in
    # assumes that shop and all products already exist
    for product in products_list:
        # product = {'id': 50, 'quantity': 10}
        # line below might not work, needs to be tested
        try:
            shop_db = MobileserverShop.objects.get(pk=shop_id)
            product_db = MobileserverProduct.objects.get(pk=product['id'])
            inventory_product = MobileserverShopproductinventory.objects.get(shop=shop_db, product=product_db)
        except ObjectDoesNotExist:
            return JSONResponse({'error': 'Either shop or product do not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        inventory_product.stock -= product['quantity']
        # timestamp will be updated on save
        inventory_product.save()

    # need to change the type of the response
    return JSONResponse({'success'})
