from django.contrib import admin

from customers.models import Customers, CustomerWallet

# Register your models here.

admin.site.register(Customers)
admin.site.register(CustomerWallet)
