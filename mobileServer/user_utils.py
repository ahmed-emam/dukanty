from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from mobileServer.serializer import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def add_address(request, order=None):
    print("******REQUEST*******")
    print(request.body)
    print(request.user)
    print("*********************")
    user = request.user

    if 'user_email' not in request.POST:
        return JSONResponse({'error': 'parameters are not complete'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if user.is_anonymous():
        try:

            user_email = request.POST.get('user_email')
            try:
                user = UsersCustomUser.objects.get(email=user_email)

            except ObjectDoesNotExist:
                return JSONResponse({'error': 'user does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return JSONResponse({'error': 'request is missing parameters'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        name = request.POST.get('name')
        street = request.POST.get('street')
        building = request.POST.get('building')
        type = request.POST.get('type')
        phone_number = request.POST.get('phone_number')
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

    if "extra_directions" in request.POST:
        extra_directions = request.POST.get('extra_directions')
    else:
        extra_directions = None

    address = Address(type=int(type), lat=lat, lon=lon, name=name, street=street, building=building, floor=floor,
                      phone_number=phone_number, apartment=apartment, extra_directions=extra_directions, owner=user)
    address.save()

    if order is not None:
        order.address = address
        order.save()

    serializedData = AddressSerializer(address)
    return JSONResponse(serializedData.data, status=status.HTTP_200_OK)

@csrf_exempt
def edit_address(request):
    if 'address_id' not in request.POST:
        return JSONResponse({'error': 'request is missing parameters'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        address_id = request.POST.get('address_id')
        try:
            address = Address.objects.get(pk=address_id)
        except ObjectDoesNotExist:
            return JSONResponse({'error': 'address does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if "lat" in request.POST:
        address.lat = float(request.POST.get('lat'))
    if "lon" in request.POST:
        address.lon = float(request.POST.get('lon'))
    if "name" in request.POST:
        address.name = request.POST.get('name')
    if "street" in request.POST:
        address.street = request.POST.get('street')
    if "floor" in request.POST:
        address.floor = request.POST.get('floor')
    if "apartment" in request.POST:
        address.apartment = request.POST.get('apartment')
    if "building" in request.POST:
        address.building = request.POST.get('building')
    if "type" in request.POST:
        address.type = request.POST.get('type')
    if "phone_number" in request.POST:
        address.phone_number = request.POST.get('phone_number')
    if "extra_directions" in request.POST:
        address.extra_directions = request.POST.get('extra_directions')
    address.save()
    return JSONResponse({}, status=status.HTTP_200_OK)


def del_address(request):
    if 'address_id' not in request.POST:
        return JSONResponse({'error': 'request is missing parameters'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        address_id = request.POST.get('address_id')
        try:
            address = Address.objects.get(pk=address_id)
            address.delete()
            return JSONResponse({}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return JSONResponse({'error': 'address does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


def get_address_by_user_mail(request):
    if "user_email" not in request.POST:
        return JSONResponse({'error': 'request is missing parameters'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        user_email = request.POST.get('user_email')
        try:
            user = UsersCustomUser.objects.get(email=user_email)
        except ObjectDoesNotExist:
            return JSONResponse({'error': 'user does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        address_list = user.address_set.all()
        serializer = AddressSerializer(address_list, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((AllowAny,))
def get_user_details(request):
    print("******REQUEST*******")
    print(request.body)
    print(request.user)
    print("*********************")
    user = request.user
    if user is not None and not user.is_anonymous():
        jsonResponse = {'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name,
                        'phone_number': user.phone_number}
        return JSONResponse(jsonResponse, status=status.HTTP_200_OK)
    else:
        return JSONResponse({'error': 'user not authorized'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)