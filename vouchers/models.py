from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from restaurants.models import RestaurantBranches, Restaurant
from customers.models import Customers

# Create your models here.
class Vouchers(models.Model):
    title = models.CharField(max_length=50, null=False)
    buy_price = models.IntegerField(validators=[MinValueValidator(10)])
    get_price = models.IntegerField(validators=[MaxValueValidator(5000)])
    # created_by = models.ForeignKey(RestaurantBranches, on_delete=models.CASCADE, null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False, blank=False)
    is_global = models.BooleanField(default=True) 
    expire_at = models.DateField(null=False)
    archived = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)+'_'+self.title+'_'+str(self.buy_price)+'_'+str(self.get_price)

class VoucherRestaurantMap(models.Model):
    voucher =  models.ForeignKey(Vouchers, on_delete=models.CASCADE, null=False, blank=False)
    restaurant_branch = models.ForeignKey(RestaurantBranches, on_delete=models.CASCADE, null=False, blank=False)
    archived = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.voucher.title+'_'+self.restaurant_branch.restaurant.name

class VoucherHistory(models.Model):
    voucher_id = models.ForeignKey(Vouchers, on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=False)
    redeemed = models.BooleanField(default=False, null=False)
    purchased_at = models.DateField(auto_now_add=True)
    redeemed_at = models.DateField(default=None, null=True, blank=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.voucher_id.title+'_'+self.customer.first_name+'_'+str(self.voucher_id.expire_at)