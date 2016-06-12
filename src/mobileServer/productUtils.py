import StringIO
import os
from zipfile import ZipFile

from django.core.exceptions import *
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.renderers import JSONRenderer

from mobileServer.error import *
from mobileServer.serializer import *


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


"""
@api {GET} getproducts/ Get All products
@apiVersion 1.0.0
@apiName ListProducts
@apiGroup Products

@apiSuccess {Object[]} products_list All products

"""
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

"""
@api {post} debug/addproduct/ Add product to list of products
@apiVersion 1.0.0
@apiName AddProducts
@apiGroup Products

@apiDescription Add a product to our universal database of products, each product has a unique id which is it's
commercial barcode

@apiParam {String} barcode Product's commercial unique barcode
@apiParam {String} name Product's name
@apiParam {String} company Product's manufacturer name
@apiParam {String} category Products' category


@apiSuccess {String} added product name
@apiPermission admin
"""
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAdminUser,))
def add_product(request):
    #print(request)
    print(request.body)
    product_id = request.POST.get('barcode')
    product_name = request.POST.get('name')
    product_company = request.POST.get('company')
    product_category = request.POST.get('category')
    # product_img = request.POST.get('img')
    # shop = json.loads(request.body)
    print(product_name)
    product = MobileserverProduct.objects.create\
        (id=product_id, name=product_name, company=product_company, category=product_category)
    product.save()
    if product.id:
        print("Added product id "+str(product.id))
        return JSONResponse({'added': product_name}, status=status.HTTP_200_OK)
    else:
        print("Didnt add "+product_name)
        return JSONResponse({'error': 'couldnt add'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
@api {post} addimage/ Upload an image for a product
@apiVersion 1.0.0
@apiName AddImage
@apiGroup Products

@apiDescription Use it to a link an image with a product, the uploaded image will be link to the product specified by
product_id

@apiParam {String} product_id Product's commercial unique barcode
@apiParam {File} file   The image uploaded as a file


@apiSuccess {String} Success Added image for <code>product_id</code>

@apiUse ProductNotFoundError
"""
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAdminUser,))
def add_image(request, product_id=None):
    if product_id is None:
        product_id = request.POST.get('product_id')

    image_file = request.FILES['file']
    print("Adding image "+image_file.name+" for "+product_id)
    try:
        product = MobileserverProduct.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        return JSONResponse({'error': ProductNotFound}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    image = Image(product=product, image=image_file,
                  mimeType=image_file.content_type)
    image.save()
    print("Added "+image.product.name)
    return JSONResponse({'Success': "Added image for "+product_id}, status=status.HTTP_200_OK)

"""
@api {get} getimage/:product_id Get image by ID
@apiVersion 1.0.0
@apiName GetImage
@apiGroup Products

@apiDescription Get image linked to product with 'product_id'


@apiSuccess {File} Image    The image as a file

"""
def getImage(request, image_id):
    i = Image.objects.get(product=image_id)
    return HttpResponse(i.image.read(), content_type=i.mimeType)

"""
@api {post} getimages/  Get images from list of IDs
@apiVersion 1.0.0
@apiName GetImages
@apiGroup Products

@apiDescription Get bulk of images at once from list of product IDs as a compressed archive

@apiParam {String[]} product_list   list of product IDs

@apiSuccess {File} Image    list of images in a compressed archive

@apiUse ReqParamMiss
"""
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((AllowAny,))
def getImages(request):
    if 'product_list' not in request.POST:
        return JSONResponse({'error': MissingParameter}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    product_list = request.POST.getlist('product_list')
    print(product_list)
    #product_list = json.loads(product_list)

    # zip_subdir = "somefiles"
    # zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()


    # The zip compressor
    zf = ZipFile(s, "w")

    for product_id in product_list:
        image = Image.objects.get(product=int(product_id))
        # Calculate path for file in zip
        fdir, fname = os.path.split(str(image.image.file))
        # zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(str(image.image.file), fname)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    return HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")


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



