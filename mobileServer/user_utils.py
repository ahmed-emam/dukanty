from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from mobileServer.serializer import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import *

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def add_address(request, order=None):
    print("******REQUEST*******")
    print(request.body)
    print(request.user)
    print("*********************")
    user = request.user

    if 'user_id' not in request.POST:
        return JSONResponse({'error': 'parameters are not complete'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    if user.is_anonymous():
        try:

            user_id = request.POST.get('user_id')
            try:
                user = UsersCustomUser.objects.get(pk=user_id)

            except ObjectDoesNotExist:
                return JSONResponse({'error': 'user does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return JSONResponse({'error': 'request is missing parameters'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        street = request.POST.get('street')
        building = request.POST.get('building')
        type = request.POST.get('type')
    except KeyError:
        return JSONResponse({'error': 'request is missing parameters'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if "floor" in request.POST:
        floor = request.POST.get('floor')
    else:
        floor = None
    if "apartment" in request.POST:
        apartment = request.POST.get('apartment')
    else:
        apartment = None
    address = Address(type=int(type), lat=lat, lon=lon, street=street, building=building,
                      floor=floor, apartment=apartment, owner=user)

    address.save()

    if order is not None:
        order.address = address
        order.save()

    serializedData = AddressSerializer(address)
    return JSONResponse(serializedData.data, status=status.HTTP_200_OK)

def get_address_by_user_id(request):
    print("******REQUEST*******")
    print(request.body)
    print(request.user)
    print("*********************")
    user = request.user
    if user.is_anonymous():
        try:

            user_id = request.POST.get('user_id')
            try:
                user = UsersCustomUser.objects.get(pk=user_id)


            except ObjectDoesNotExist:
                return JSONResponse({'error': 'user does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return JSONResponse({'error': 'request is missing parameters'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    address_list = user.address_set.all()
    serializer = AddressSerializer(address_list, many=True)
    return JSONResponse(serializer.data)