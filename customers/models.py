from datetime import datetime
from django.db import models

# from vouchers import models as VoucherModels

# Create your models here.
class Customers(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    contact_number = models.IntegerField(null=False, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.first_name+' '+self.last_name

class CustomerWallet(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    value = models.IntegerField()
    medium = models.CharField(max_length=20, null=False, blank=False)
    # Getting Circular Import error here, need to fix later
    # voucher = models.ForeignKey(VoucherModels.Vouchers, blank=True, null=True)
    voucher = models.IntegerField()
    redeemed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.medium+'_'+str(self.value)