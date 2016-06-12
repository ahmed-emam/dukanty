# This is an API for santizing input from user and querying from database.
#
# This wrapper raises the appropriate exceptions once an inappropriate request
# 	is received. The exceptions defined are handled by exception_handler.py.
#
#

from mobileServer.models import *
from mobileServer.exceptions import *


"""
You want want data=request.data and key to be the parameter as 'shop_id'
"""
def get_parameter(data, key):
	param = data[key]

	if param is None:
		raise MissingParameter

	return param

# QUERIES Wrapper

def query_MobileserverShop(**kwards):
	try:
		query = MobileserverShop.objects.get(**kwards)
	except Exception:
		raise ShopNotFound	

	return query

def query_MobileserverProduct(**kwards):
	try:
		query = MobileserverProduct.objects.get(**kwards)
	except Exception:
		raise ProductNotFound
	return query

def query_MobileserverShopproductinventory(**kwards):
	try:
		query = MobileserverShopproductinventory.objects.get(**kwards)
	except Exception:
		raise GenericException

	return query

def query_Image(**kwards):
	try:
		query = Image.objects.get(**kwards)
	except Exception:
		raise ProductImageNotUploaded

	return query
