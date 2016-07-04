from django.core.exceptions import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from mobileServer.error import *
from mobileServer.serializer import *
from mobileServer.models import *
from users.models import UsersCustomUser

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


"""
@api {post} add_address/ Add address for user
@apiVersion 1.0.0
@apiName AddAddress
@apiGroup User

@apiParam {String} user_email User's email
@apiParam {Number} lat Latitude of added address
@apiParam {Number} lon Longitude of added address
@apiParam {String} name Given title for added address
@apiParam {String} street street number/name
@apiParam {String} building building number/name
@apiParam {Number} type House==1/Building==2
@apiParam {String} phone_number Phone number to call on
@apiParam {String} zone Address's Zone id/name
@apiParam {String} [floor] Floor Number for addresses of type=building
@apiParam {String} [apartment] Apartment number for addresses of type=building
@apiParam {String} [extra_directions] Additional info


@apiSuccess {Object} address serialized data of newly added address

@apiUse UserNotFoundError
@apiUse ReqParamMiss
"""
@api_view(['POST'])
@permission_classes((AllowAny,))
def add_address(request, order=None):
    print("******REQUEST*******")
    print(request.body)
    print(request.user)
    print("*********************")
    user = request.user

    if 'user_email' not in request.POST:
        return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if user.is_anonymous():
        try:

            user_email = request.POST.get('user_email')
            try:
                user = UsersCustomUser.objects.get(email=user_email)

            except ObjectDoesNotExist:
                return JSONResponse({'error': 'user does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        name = request.POST.get('name')
        street = request.POST.get('street')
        building = request.POST.get('building')
        type = request.POST.get('type')
        phone_number = request.POST.get('phone_number')
        zone = request.POST.get('zone')
    except KeyError:
        return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    address = Address(type=int(type), lat=lat, lon=lon, name=name, street=street, building=building,
                      floor=floor, zone=zone,
                      phone_number=phone_number, apartment=apartment, extra_directions=extra_directions, owner=user)
    address.save()

    if order is not None:
        order.address = address
        order.save()

    serializedData = AddressSerializer(address)
    return JSONResponse(serializedData.data, status=status.HTTP_200_OK)


"""
@api {post} editAddress/ edit address for user
@apiVersion 1.0.0
@apiName EditAddress
@apiGroup User

@apiParam {Number} address_id Address unique id
@apiParam {Number} [lat] Latitude of added address
@apiParam {Number} [lon] Longitude of added address
@apiParam {String} [name] Given title for added address
@apiParam {String} [street] street number/name
@apiParam {String} [building] building number/name
@apiParam {Number} [type] House==1/Building==2
@apiParam {String} [phone_number] Phone number to call on
@apiParam {String} [zone] Address's Zone id/name
@apiParam {String} [floor] Floor Number for addresses of type=building
@apiParam {String} [apartment] Apartment number for addresses of type=building
@apiParam {String} [extra_directions] Additional info

@apiSuccess {Object} null

@apiUse AddressNotFoundError
@apiUse ReqParamMiss
"""
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((AllowAny,))
def edit_address(request):
    if 'address_id' not in request.POST:
        return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        address_id = request.POST.get('address_id')
        try:
            address = Address.objects.get(pk=address_id)
        except ObjectDoesNotExist:
            return JSONResponse({'error': address_id+' does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    if "zone" in request.POST:
        address.zone = request.POST.get('zone')
    address.save()
    return JSONResponse({}, status=status.HTTP_200_OK)


"""
@api {post} delAddress/ delete address for user
@apiVersion 1.0.0
@apiName DelAddress
@apiGroup User

@apiParam {Number} address_id Address unique id

@apiSuccess {Object} null

@apiUse AddressNotFoundError
@apiUse ReqParamMiss


"""
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((AllowAny,))
def del_address(request):
    if 'address_id' not in request.POST:
        return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        address_id = request.POST.get('address_id')
        try:
            address = Address.objects.get(pk=address_id)
            address.delete()
            return JSONResponse({}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return JSONResponse({'error': address_id+' does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
@api {post} getAddresses/ Get List of Addresses for user
@apiVersion 1.0.0
@apiName GetAddress
@apiGroup User

@apiParam {Number} user_id User unique id

@apiSuccess {Object} Serialized data of address

@apiUse UserNotFoundError
@apiUse ReqParamMiss
@apiUse IsAuthenticated


@apiPermission AuthenticatedUser
"""
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_address_by_user_id(request):
    """
    Get List of addresses saved by the user
    """
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
                return JSONResponse({'error': user_id+' does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    address_list = user.address_set.all()
    serializer = AddressSerializer(address_list, many=True)
    return JSONResponse(serializer.data)

@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((AllowAny,))
def get_address_by_user_mail(request):
    if "user_email" not in request.POST:
        return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        user_email = request.POST.get('user_email')
        try:
            user = UsersCustomUser.objects.get(email=user_email)
        except ObjectDoesNotExist:
            return JSONResponse({'error': 'user does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        address_list = user.address_set.all()
        serializer = AddressSerializer(address_list, many=True)
        return JSONResponse(serializer.data)


"""
@api {get, post} getUserDetails/ Get User details

@apiVersion 1.0.0
@apiName GetUser
@apiGroup User


@apiSuccess {String} id User unique id
@apiSuccess {String} email User's email
@apiSuccess {String} first_name User's first name
@apiSuccess {String} last_name User's last name
@apiSuccess {String} phone_number User's phone number


@apiUse NotAuthorized
@apiUse IsAuthenticated

@apiPermission AuthenticatedUser
"""
@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_user_details(request):
    print("******REQUEST*******")
    print(request.body)
    print(request.user)
    print("*********************")
    user = request.user
    if user is not None and not user.is_anonymous():
        listofshops = ShopSerializer(user.mobileservershop_set.all(), many=True)
        jsonResponse = {'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name,
                        'phone_number': user.phone_number, 'shop_ids': listofshops}
        return JSONResponse(jsonResponse, status=status.HTTP_200_OK)
    else:
        return JSONResponse({'error': 'user not authorized'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
@api {post} editUserDetails/ Edit User details

@apiVersion 1.0.0
@apiName GetUser
@apiGroup User

@apiParam {Number} phone_number User's Phone number
@apiParam {String} first_name   User's first name
@apiParam {String} last_name    User's Last name

@apiSuccess {String} success    Details has been changed

@apiUse NotAuthorized
@apiUse IsAuthenticated

@apiPermission AuthenticatedUser
"""
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def edit_user_details(request):
    print("******REQUEST*******")
    print(request.body)
    print(request.user)
    print("*********************")
    user = request.user
    # if 'phone_number' not in request.POST and 'first_name' not in request.POST and 'last_name' not in request.POST:
    #     return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if user is None or user.is_anonymous():
        return JSONResponse({'error': NotAuthorized}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if 'phone_number' in request.POST:
        phone_number = request.POST.get['phone_number']
        user.phone_number = phone_number

    if 'first_name' in request.POST:
        first_name = request.POST.get['first_name']
        user.first_name = first_name

    if 'last_name' in request.POST:
        last_name = request.POST.get['last_name']
        user.last_name = last_name

    user.save()
    return JSONResponse({}, status=status.HTTP_200_OK)