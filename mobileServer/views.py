from django.shortcuts import render
from rest_framework import viewsets
from mobileServer.models import *
from mobileServer.serializer import ShopSerializer

# Create your views here.
def index(request):
    page = render(request, "index.html", {})
    return page

def getshops(request):
    return


# ViewSets define the view behavior.
class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer