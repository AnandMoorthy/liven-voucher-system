from django.contrib import admin

from restaurants.models import Restaurant, RestaurantBranches, RestaurantCity

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(RestaurantBranches)
admin.site.register(RestaurantCity)
