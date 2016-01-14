from django.contrib import admin
from mobileServer.models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group

# class MyUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = MyUser
#
# class MyUserAdmin(UserAdmin):
#     form = MyUserChangeForm
#
#     fieldsets = UserAdmin.fieldsets + (
#             (None, {'fields': ('some_extra_data',)}),
#     )

# Register your models here.
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(ShopInventory)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Basket)
admin.site.register(ShopProductInventory)
#admin.site.unregister(Group)