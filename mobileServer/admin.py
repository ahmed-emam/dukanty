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
admin.site.register(MobileserverShop)
admin.site.register(MobileserverProduct)
# admin.site.register(MobileserverShopinventory)
admin.site.register(MobileserverCart)
admin.site.register(MobileserverCartitem)
admin.site.register(MobileserverBasket)
admin.site.register(MobileserverShopproductinventory)
admin.site.register(MobileserverOrder)
admin.site.register(MobileserverOrderProduct)

# admin.site.register(MobileserverShopinventoryProduct)
#admin.site.unregister(Group)