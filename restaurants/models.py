import uuid
from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255, null=False) 
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name+'_'+str(self.id)

class RestaurantCity(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    zipcode = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name+'_'+self.state+'_'+str(self.zipcode)

class RestaurantBranches(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    address = models.TextField(max_length=255, null=False)
    unique_id = models.CharField(max_length=20, null=False, unique=True, default=uuid.uuid4().hex[:8])
    city = models.ForeignKey(RestaurantCity, on_delete=models.CASCADE, default=None, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.restaurant.name +'_'+ self.unique_id+'_'+str(self.id)