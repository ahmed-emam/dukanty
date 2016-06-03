from rest_framework.exceptions import APIException

# Generic exception

class GenericException(APIException):
    status_code = 500
    default_detail = 'Generic Exception'

# User related exceptions

class MissingParameter(APIException):
    status_code = 500
    default_detail = '100 - Missing a parameter'

class ParameterTypeInvalid(APIException):
    status_code = 500
    default_detail = '101 - Parameter type is invalid'

# Shop related exceptions

class ShopNotFound(APIException):
    status_code = 500
    default_detail = '200 - Shop is not found'

class ShopLatLongExist(APIException):
    status_code = 500
    default_detail = '201 - Shop latitude and longtitude exists'

class InvalidLatLong(APIException):
    status_code = 500
    default_detail = '202 - Invalid latitude and longtitude'

class DeliverDistanceInvalid(APIException):
    status_code = 500
    default_detail = '203 - Delivery Distance is invalid (maybe you are too far\
    							or shop does not deliver)'

class RatingInvalid(APIException):
    status_code = 500
    default_detail = '204 - Invalid Rating'

class StockInvalid(APIException):
    status_code = 500
    default_detail = '205 - Invalid Stock'

class InventoryNotFound(APIException):
    status_code = 500
    default_detail = '205 - Inventory is not found'

class ShopExists(APIException):
    status_code = 500
    default_detail = '207 - Shop exists'


# Product related exceptions 

class ProductNotFound(APIException):
    status_code = 500
    default_detail = '300 - Product is not found'

class ProductImageNotUploaded(APIException):
    status_code = 500
    default_detail = '301 - Image for the product is not uploaded'

class ProductExists(APIException):
    status_code = 500
    default_detail = '302 - Product exists'