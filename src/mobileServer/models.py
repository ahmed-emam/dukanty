from django.db import models
from taggit.managers import TaggableManager
from users.models import UsersCustomUser
from django.utils.translation import ugettext_lazy as _
import uuid

# User = get_user_model()
#
 
 
 
 
class MobileserverBasket(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey('users.UsersCustomuser', models.DO_NOTHING)
    cart = models.ForeignKey('MobileserverCart', models.DO_NOTHING, blank=True, null=True)
 
    class Meta:
        db_table = 'mobileServer_basket'
 
 
class MobileserverCart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField()
    owner = models.ForeignKey('users.UsersCustomuser')

    class Meta:
        db_table = 'mobileServer_cart'
 
 
class MobileserverCartitem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    cart = models.ForeignKey(MobileserverCart, on_delete=models.CASCADE)
    product = models.ForeignKey('MobileserverShopproductinventory', models.DO_NOTHING)
 
    class Meta:
        db_table = 'mobileServer_cartitem'


ADDRESS_TYPES = [
  (1, _("House")),
  (2, _("Building")),
]
class Address(models.Model):
    type = models.IntegerField(choices=ADDRESS_TYPES)
    lat = models.FloatField()
    lon = models.FloatField()
    name = models.CharField(max_length=30)
    phone_number = models.CharField(_('Phone Number'), max_length=8)
    zone = models.CharField(max_length=30)
    street = models.CharField(max_length=90)
    building = models.CharField(max_length=90)
    floor = models.CharField(max_length=30, null=True)
    apartment = models.CharField(max_length=30, null=True)
    extra_directions = models.TextField(null=True)

    owner = models.ForeignKey('users.UsersCustomuser', models.CASCADE)

    class Meta:
        db_table = 'Address'


'''
status:
0 -> not ordered
1 -> order issued
2 -> order on delivery
3 -> order delivered
4 -> order cancelled
'''
class MobileserverOrder(models.Model):
   # order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    totalprice = models.FloatField(db_column='totalPrice', default=0.0)  # Field name made lowercase.
    name = models.CharField(max_length=30)
    phone_number = models.CharField(_('Phone Number'), max_length=8)
    owner = models.ForeignKey('users.UsersCustomuser', on_delete=models.CASCADE)
    shop = models.ForeignKey('MobileserverShop', models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(default=0)
    address = models.ForeignKey(Address, models.SET_NULL, null=True)

    class Meta:
        db_table = 'mobileServer_order'
 
    def __str__(self):
        return self.id.__str__()+"\tOwner:"+self.owner.__str__()+\
               "\tFrom:"+self.shop.__str__()+"\tStatus:"+self.status.__str__()
 

class MobileserverOrderProduct(models.Model):
    order = models.ForeignKey(MobileserverOrder, models.CASCADE)
    product = models.ForeignKey('MobileserverProduct', models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    price = models.FloatField(default=0.0)

    class Meta:
        db_table = 'mobileServer_order_product'
 
'''
Model representation of a product


TODO: Add

Category:
1 -> Beverages
2 -> Bakery
3 -> Dairy
4 -> Produce
5 -> canned food
6 -> chocolate
7 -> Health & Beauty
8 -> Spices
'''
class MobileserverProduct(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=90)
    company = models.CharField(max_length=90)
    category = models.PositiveSmallIntegerField()
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name+" by "+self.company
 
    class Meta:
        db_table = 'mobileServer_product'

        
class MobileserverShop(models.Model):
    name = models.CharField(max_length=30)
    rating = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    lat = models.FloatField()
    lon = models.FloatField()
    delivery_distance = models.FloatField(default=5.0)
    owner = models.ForeignKey('users.UsersCustomuser', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
 
    class Meta:
        db_table = 'mobileServer_shop'
 
    def __unicode__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(MobileserverProduct, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    mimeType = models.CharField(max_length=20)


class ShopImage(models.Model):
    shop = models.ForeignKey(MobileserverShop, unique=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shops/')
    mimeType = models.CharField(max_length=20)
#
#
# class MobileserverShopinventory(models.Model):
#     stock = models.BooleanField()
#     owner = models.ForeignKey('users.UsersCustomuser', models.DO_NOTHING, unique=True)
#     shop = models.ForeignKey(MobileserverShop, models.DO_NOTHING, unique=True)
#
#     class Meta:
#         db_table = 'mobileServer_shopinventory'
 
 
# class MobileserverShopinventoryProduct(models.Model):
#     shopinventory = models.ForeignKey(MobileserverShopinventory, models.DO_NOTHING)
#     shopproductinventory = models.ForeignKey('MobileserverShopproductinventory', models.DO_NOTHING)
#
#     class Meta:
#         db_table = 'mobileServer_shopinventory_product'
#         unique_together = (('shopinventory', 'shopproductinventory'),)
 
 
class MobileserverShopproductinventory(models.Model):
    price = models.FloatField(default=0.0)
    # what options should it take
    stock = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(MobileserverProduct, on_delete=models.CASCADE)
    shop = models.ForeignKey(MobileserverShop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mobileServer_shopproductinventory'
 
    def __str__(self):
        return self.product.name+" "+self.shop.name+" "+str(self.price)+" "+str(self.stock)

