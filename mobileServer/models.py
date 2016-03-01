from django.db import models
from taggit.managers import TaggableManager
from users.models import UsersCustomUser
from django.utils.translation import ugettext_lazy as _
 
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
 
'''
status:
0 -> not ordered
1 -> order issued
2 -> order on delivery
3 -> order delivered
'''
class MobileserverOrder(models.Model):
    totalprice = models.FloatField(db_column='totalPrice', default=0.0)  # Field name made lowercase.
    name = models.CharField(max_length=30)
    mobile = models.IntegerField()
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
Category:
0 ->
1 ->
2 ->
3 ->
'''
class MobileserverProduct(models.Model):
    name = models.CharField(max_length=30)
    company = models.CharField(max_length=30)
    category = models.PositiveSmallIntegerField()
    img = models.TextField()
    tags = TaggableManager()
 
    def __str__(self):
        return self.name+" by "+self.company
 
    class Meta:
        db_table = 'mobileServer_product'


ADDRESS_TYPES = [
  (1, _("Villa")),
  (2, _("Building")),
]

class Address(models.Model):
    type = models.IntegerField(choices=ADDRESS_TYPES)
    lat = models.FloatField()
    lon = models.FloatField()
    street = models.CharField(max_length=90)
    building = models.CharField(max_length=90)
    floor = models.CharField(max_length=30, null=True)
    apartment = models.CharField(max_length=30, null=True)
    owner = models.ForeignKey('users.UsersCustomuser', models.CASCADE)

    class Meta:
        db_table = 'Address'
        
class MobileserverShop(models.Model):
    name = models.CharField(max_length=30)
    rating = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    lat = models.FloatField()
    lon = models.FloatField()
    delivery_distance = models.FloatField(default=5.0)

    def __str__(self):
        return self.name
 
    class Meta:
        db_table = 'mobileServer_shop'
 
    def __unicode__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(MobileserverProduct, unique=True)
    image = models.ImageField(upload_to='products/')
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
    stock = models.BooleanField(default=True)
    product = models.ForeignKey(MobileserverProduct, on_delete=models.CASCADE)
    owner = models.ForeignKey('users.UsersCustomuser', on_delete=models.CASCADE)
    shop = models.ForeignKey(MobileserverShop, on_delete=models.CASCADE)


    class Meta:
        db_table = 'mobileServer_shopproductinventory'
 
    def __str__(self):
        return self.product.name+" "+self.shop.name+" "+str(self.price)+" "+str(self.stock)


'''
 
# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=30)
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    lat = models.FloatField()
    lon = models.FloatField()
 
    def __str__(self):
        return self.name+" ("+self.lat.__str__()+","+self.lon.__str__()+")"
 
 
'''
# Category:
# 1 ->
# 2 ->
# 3 ->
 
'''
class Product(models.Model):
    name = models.CharField(max_length=30)
    company = models.CharField(max_length=30)
    img = models.TextField(max_length=100)
    category = models.IntegerField()
    tags = TaggableManager()
 
    def __str__(self):
        return self.name+" by "+self.company
 
    def natural_key(self):
        return self.name, self.company, self.img, self.category
 
 
'''
# Class represents a cart, which can represent an order or a basket
'''
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
 
    # User that owns the cart
    owner = models.ForeignKey(CustomUser)
 
    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('created_at',)
 
    def __unicode__(self):
        return self.creation_date
 
    def __str__(self):
        return "Created at:"+str(self.created_at)
 
    def natural_key(self):
        return self.cartitem_set.natural_key()
 
 
"""
TODO: Check what does order represent....do I need it or cart is enoughauth_group_permissions
"""
class Order(models.Model):
    product = models.ManyToManyField(Product)
    owner = models.ForeignKey(CustomUser)
    totalPrice = models.FloatField()
    shop = models.OneToOneField(Shop)
 
 
class ShopProductInventory(models.Model):
    product = models.ForeignKey(Product)
    price = models.FloatField()
 
    def __str__(self):
        return str(self.product)+" for "+str(self.price)
 
 
class CartItem(models.Model):
    # a link to the cart that this item lives in
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    quantity = models.PositiveIntegerField()
    # unit_price = models.DecimalField(max_digits=18, decimal_places=2)
    # # a link to the product this item represent
    # product = models.ForeignKey(Product)
    product = models.ForeignKey(ShopProductInventory)
 
    class Meta:
        verbose_name = _('cartItem')
 
    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)
 
    def natural_key(self):
        return self.quantity, self.product.natural_key()
 
    # product
    def get_product(self):
        return Product.objects.get(pk=self.product.id)
 
    def __str__(self):
        return str(self.cart)+" "+str(self.product)+" "+str(self.quantity)
    # def set_product(self, product):
    #     self.content_type = ContentType.objects.get_for_model(type(product))
    #     self.object_id = product.pk
    #
    # product = property(get_product, set_product)
 
 
"""
A shop inventory is a list of products that are linked to a specific shop
"""
class ShopInventory(models.Model):
    product = models.ManyToManyField(ShopProductInventory)
    shop = models.OneToOneField(Shop)
    stock = models.BooleanField(default=True)
    # Shop owner
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
 
    def __str__(self):
        return str(self.product)+" @ "+str(self.shop)+" "+str(self.stock)
 
    def natural_key(self):
        return self.stock
 
 
class Basket(models.Model):
    name = models.CharField(max_length=30)
    cart = models.ForeignKey(Cart, null=True)
    owner = models.ForeignKey(CustomUser)
 
    def natural_key(self):
        return (self.name,) + self.cart.natural_key()

'''