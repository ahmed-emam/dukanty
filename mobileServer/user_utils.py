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
    if user.is_anonymous():
        try:

            user_id = request.POST.get('user_id')
            try:
                user = UsersCustomUser.objects.get(pd=user_id)

            except ObjectDoesNotExist:
                return JSONResponse({'error': 'user does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return JSONResponse({'error': 'request is missing parameters'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        street = request.POST.get('street')
        building = request.POST.get('building')

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
    address = Address(lat=lat, lon=lon, street=street, building=building,
                      floor=floor, apartment=apartment, owner=user, order=order)
    address.save()

    serializedData = AddressSerializer(address)
    return JSONResponse(serializedData.data, status=status.HTTP_200_OK)