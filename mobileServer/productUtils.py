from django.shortcuts import render
from rest_framework import viewsets
from mobileServer.models import *
from users.models import  *
from mobileServer.serializer import *
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, permissions, status, response, views
from rest_framework.response import Response
from django.core.exceptions import *
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import os, tempfile, StringIO
from zipfile import ZipFile
#from django.core.servers.basehttp import FileWrapper


import json

from django.core.exceptions import *


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
def products_list(request):
    if request.method == 'GET':
        products = MobileserverProduct.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JSONResponse(serializer.data)
    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = SnippetSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JSONResponse(serializer.data, status=201)
    #     return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def add_product(request):
    #print(request)
    print(request.body)
    product_name = request.POST.get('name')
    product_company = request.POST.get('company')
    product_category = request.POST.get('category')
    product_img = request.POST.get('img')
    # shop = json.loads(request.body)
    print(product_name)
    product = MobileserverProduct.objects.create\
        (name=product_name, company=product_company, category=product_category, img=product_img)
    product.save()
    if product.id:
        print("Added shop id "+str(product.id))
        return JSONResponse({'added': product_name}, status=status.HTTP_200_OK)
    else:
        print("Didnt add "+product_name)
        return JSONResponse({'error': 'couldnt add'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def add_image(request, product_id=None):
    if product_id is None:
        product_id = request.POST.get('product_id')

    image_file = request.FILES['file']
    print "Adding image "+image_file.name+" for "+product_id
    try:
        product = MobileserverProduct.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        return JSONResponse({'error': 'product doesnt exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    image = Image(product=product, image=image_file,
                  mimeType=image_file.content_type)
    image.save()
    print "Added "+image.product.name
    return JSONResponse({'Success': "Adding image for "+product_id}, status=status.HTTP_200_OK)

def getImage(request, image_id):
    i = Image.objects.get(product=image_id)
    return HttpResponse(i.image.read(), content_type=i.mimeType)


@csrf_exempt
def getImages(request):
    if 'product_list' not in request.POST:
        return JSONResponse({'error': 'parameters are not complete'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    product_list = request.POST.getlist('product_list')
    print product_list
    #product_list = json.loads(product_list)

    zip_subdir = "somefiles"
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    for product_id in product_list:
        fdir, fname = os.path.split(fpath)
        print fdir+" "+fname
        zip_path = os.path.join(zip_subdir, fname)
        print zip_path
    # The zip compressor
    # zf = zipfile.ZipFile(s, "w")
    #
    # for fpath in filenames:
    #     # Calculate path for file in zip
    #     fdir, fname = os.path.split(fpath)
    #     zip_path = os.path.join(zip_subdir, fname)
    #
    #     # Add file, at correct path
    #     zf.write(fpath, zip_path)
    #
    # # Must close zip for all contents to be written
    # zf.close()
    #
    # # Grab ZIP file from in-memory, make response with correct MIME-type
    # return HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")


    # print product_list
    # with ZipFile('image.zip', 'w') as myzip:
    #     for product_id in product_list:
    #         image = Image.objects.get(product=int(product_id))
    #         print image.image.file
    #         print image.image.name
    #         myzip.write(str(image.image.file))
    #         # print image.image.url
    #     myzip.close()
    #     print(myzip.printdir())
    #     return HttpResponse(myzip, content_type='application/zip')
    # return JSONResponse({}, status=status.HTTP_200_OK)



