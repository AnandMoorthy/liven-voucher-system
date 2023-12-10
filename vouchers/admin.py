from django.contrib import admin
from vouchers.models import Vouchers, VoucherHistory, VoucherRestaurantMap

# Register your models here.

admin.site.register(Vouchers)
admin.site.register(VoucherHistory)
admin.site.register(VoucherRestaurantMap)
