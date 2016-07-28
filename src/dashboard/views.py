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

from rest_framework import permissions, request
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.http import HttpResponseRedirect
from django.core.exceptions import *
from django.template.loader import get_template
import json
import csv


"""
The search can be done using a trie or BST

"""
def remove_duplicates(lst):
    result = []
    
    for e in lst:
        if e.strip() not in result:
            result.append(e)

    return result

"""
parse_sales: expects a list of MobileserverOrderProduct
             returns a list of objects such as 
                [{"date": x, "price": y}]

"""
def parse_sales(data_model):
    result = []

    for record in data_model:
        result.append(\
            {"price" : record.price,
             "data" : record.order.updated_at\
             })\

    return result

"""
I will have have to change the code below once 

"""
def index(request): 
    # supp = UsersCustomUser.objects.filter()
    # orders = MobileserverOrderProduct.objects.filter()
    products = MobileserverProduct.objects.filter()
    companies = [product.company for product in products]
    companies = remove_duplicates(companies)
    return render(request, "dashboard_index.html", {"suppliers": companies})

"""
get_sales: expects the name of the supplier 
           returns a page with graphed data 

"""
def get_sales(request, supp_name):
    # get all the products for given supplier
    products_for_supp = MobileserverProduct.objects.filter(company=supp_name)
    # get all orders for the supplier's products
    all_sales = MobileserverOrderProduct.objects.filter(product__in=products_for_supp)
    # parse the sales to be returned to the user
    sales = parse_sales(all_sales)

    return render(request, "dashboard_plot.html", {"data": sales})

def sales(request):
    mock = "date,close\n1-May-12,58.13\n30-Apr-12,53.98\n27-Apr-12,67.00\n26-Apr-12,89.70\n25-Apr-12,99.00\n24-Apr-12,130.28\n23-Apr-12,166.70\n20-Apr-12,234.98\n19-Apr-12,345.44\n18-Apr-12,443.34\n17-Apr-12,543.70\n16-Apr-12,580.13\n13-Apr-12,605.23\n12-Apr-12,622.77\n11-Apr-12,626.20\n10-Apr-12,628.44\n9-Apr-12,636.23\n5-Apr-12,633.68\n4-Apr-12,624.31\n3-Apr-12,629.32\n2-Apr-12,618.63\n30-Mar-12,599.55\n29-Mar-12,609.86\n28-Mar-12,617.62\n27-Mar-12,614.48\n26-Mar-12,606.98"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    
    writer = csv.writer(response)

    mock = mock.split('\n')

    for e in mock:
        parsed = e.split(',')
        writer.writerow(parsed)
    # writer.writerow(["date", "close"])
    # writer.writerow(["1-May-12", "58.13"])
    # writer.writerow(["2-May-12", "60.45"])

    return response
    