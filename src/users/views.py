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

@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def edit_details(request):
	"""
	This will need you to have to pass the email of this user
	"""

	post_data = request.data
	user = 	user = UsersCustomUser.objects.get(email=email)
	email = post_data['email']

	if(user != email):
		return JSONResponse({"edit_details": "not authorized"}, status=status.HTTP_401_UNAUTHORIZED)


	if(post_data['first_name']):
		user.first_name = post_data['first_name']
	if(post_data['last_name']):
		user.last_name = post_data['last_name']
	if(post_data['phone_number']):
		user.phone_number = post_data['phone_number']

	user.save()

	return JSONResponse({"edit_details": "sucess"}, status=status.HTTP_200_OK)
