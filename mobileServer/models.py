from django.db import models
from taggit.managers import TaggableManager
from users.models import CustomUser
from django.utils.translation import ugettext_lazy as _

# User = get_user_model()
#




class MobileserverBasket(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=30)
    owner = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)
    cart = models.ForeignKey('MobileserverCart', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'mobileServer_basket'


class MobileserverCart(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    checked_out = models.BooleanField()
    owner = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        db_table = 'mobileServer_cart'


class MobileserverCartitem(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(MobileserverCart, models.DO_NOTHING)
    product = models.ForeignKey('MobileserverShopproductinventory', models.DO_NOTHING)

    class Meta:
        db_table = 'mobileServer_cartitem'


class MobileserverOrder(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    totalprice = models.FloatField(db_column='totalPrice')  # Field name made lowercase.
    owner = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)
    shop = models.ForeignKey('MobileserverShop', models.DO_NOTHING, unique=True)

    class Meta:
        db_table = 'mobileServer_order'


class MobileserverOrderProduct(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    order = models.ForeignKey(MobileserverOrder, models.DO_NOTHING)
    product = models.ForeignKey('MobileserverProduct', models.DO_NOTHING)

    class Meta:
        db_table = 'mobileServer_order_product'


class MobileserverProduct(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=30)
    company = models.CharField(max_length=30)
    category = models.IntegerField()
    img = models.TextField()

    class Meta:
        db_table = 'mobileServer_product'


class MobileserverShop(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=30)
    rating = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    lat = models.FloatField()
    lon = models.FloatField()

    class Meta:
        db_table = 'mobileServer_shop'


class MobileserverShopinventory(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    stock = models.BooleanField()
    owner = models.ForeignKey('UsersCustomuser', models.DO_NOTHING, unique=True)
    shop = models.ForeignKey(MobileserverShop, models.DO_NOTHING, unique=True)

    class Meta:
        db_table = 'mobileServer_shopinventory'


class MobileserverShopinventoryProduct(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    shopinventory = models.ForeignKey(MobileserverShopinventory, models.DO_NOTHING)
    shopproductinventory = models.ForeignKey('MobileserverShopproductinventory', models.DO_NOTHING)

    class Meta:
        db_table = 'mobileServer_shopinventory_product'
        unique_together = (('shopinventory', 'shopproductinventory'),)


class MobileserverShopproductinventory(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    price = models.FloatField()
    product = models.ForeignKey(MobileserverProduct, models.DO_NOTHING)

    class Meta:
        db_table = 'mobileServer_shopproductinventory'







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

