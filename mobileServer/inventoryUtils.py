from django.core.exceptions import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from mobileServer.serializer import *


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
def get_shopInventory(request):
    shop_id = request.GET.get('shop_id')
    print(shop_id)
    # Get the shop using shop ID
    try:
        shop = MobileserverShop.objects.get(pk=shop_id)

    except ObjectDoesNotExist:
        return JSONResponse({'error': shop_id+' does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Get all inventory entries that are linked to that shop
    inventory = MobileserverShopproductinventory.objects.filter(shop=shop)
    # Response sent back to the user
    response = []
    # loop over all the inventory entries found
    for inventoryEntry in inventory:
        related_product = inventoryEntry.product
        productSerialized = ProductSerializer(related_product)
        response.extend([{
            "product": productSerialized.data,
            "price": inventoryEntry.price,
            "stock": inventoryEntry.stock
        }])

    return JSONResponse(response)




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
    print(request.user)
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
    if stock == "False":
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


