from push_notifications.models import GCMDevice, APNSDevice
from django.core.exceptions import *
from django.http import HttpResponse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from mobileServer import error
'''
This file should manage sending notifications

'''


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def register_android_device(request):
    registrationID = request.POST.get['registrationID']
    device = GCMDevice(user=request.user, registration_id=registrationID)
    device.save()
    send_message_to_device(request.user, "You have been registered")


def send_message_to_device(user, message):
    try:
        device = GCMDevice.objects.get(user=user)
        device.send_message(message)

    except ObjectDoesNotExist:
        return JSONResponse({'error' : 'Device is not registered'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
