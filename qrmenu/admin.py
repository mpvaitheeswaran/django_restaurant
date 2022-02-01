from django.contrib import admin
from .models import AccountSetting, BillingDetail, CustomerOrder, MenuCategory,MenuItem, OrderedMenu,RestaurantDetail

# Register your models here.
admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(RestaurantDetail)
admin.site.register(OrderedMenu)
admin.site.register(CustomerOrder)
admin.site.register(BillingDetail)
admin.site.register(AccountSetting)