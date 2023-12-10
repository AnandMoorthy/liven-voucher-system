"""
URL configuration for liven_voucher_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from vouchers.views import VoucherCreateView, VoucherCustomerBuyView, VoucherCustomerRedeemView, VoucherListView
from customers.views import ListCustomerWallet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/voucher/', VoucherCreateView.as_view(), name='voucher_create'),
    path('api/voucher/customer/', VoucherListView.as_view(), name='customer_vouchers'),
    path('api/voucher/customer/', VoucherCustomerBuyView.as_view(), name='buy_voucher_for_customer'),
    path('api/voucher/customer/redeem', VoucherCustomerRedeemView.as_view(), name='redeem_voucher')
]
