from django.shortcuts import render
from rest_framework import viewsets
from mobileServer.models import *
from mobileServer.serializer import ShopSerializer
from rest_framework.decorators import api_view
# Create your views here.
def index(request):
    page = render(request, "index.html", {})
    return page

def getshops(request):
    return

#
# @api_view(['GET'])
# ViewSets define the view behavior.
class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer