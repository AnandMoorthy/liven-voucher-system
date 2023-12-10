# views.py
from datetime import datetime

from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from restaurants.models import Restaurant, RestaurantBranches
from customers.models import Customers, CustomerWallet
from vouchers.models import VoucherHistory, VoucherRestaurantMap, Vouchers

from .serializers import VoucherSerializer, CustomerVoucherSerializer


class VoucherListView(APIView):
    '''
    Listing Customers Redeemed and Non Redeemed Vouchers
    '''
    def get(self, request, *args, **kwargs):

        customer_id = request.GET.get('customer_id')

        try:
            customer = Customers.objects.get(pk=customer_id)
        except Customers.DoesNotExist:
            return Response(
                {
                    "error": "Customer not found"
                }, status=status.HTTP_404_NOT_FOUND
            )
        queryset = VoucherHistory.objects.filter(customer=customer)
        serializer = CustomerVoucherSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VoucherCreateView(APIView):
    '''
    Voucher Create API with all business logics
    '''
    def post(self, request, *args, **kwargs):
        serializer = VoucherSerializer(data=request.data)

        if serializer.is_valid():
            voucher_obj = serializer.save()
            is_global = request.POST.get('is_global')
            is_global = True if is_global == 'true' else False
            restaurants_ids = request.POST.getlist('restaurants_ids', [])
            city_ids = request.POST.getlist('city_ids', [])
            created_by = request.POST.get('created_by')
            restaurant_instance = Restaurant.objects.get(pk=created_by)
            if is_global and (len(restaurants_ids) > 0 or len(city_ids) > 0):
                return Response(
                    {
                        'message': "if is_global is true restaurants_ids and city_ids should not be passed"
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif not is_global and len(restaurants_ids) <= 0 and len(city_ids) <= 0:
                return Response(
                    {
                        'message': "Provide is_global or restaurant_ids, one of the value is required"
                    }, status=status.HTTP_400_BAD_REQUEST)
            if len(restaurants_ids) > 0 and RestaurantBranches.objects.filter(
                pk__in=restaurants_ids,
                restaurant=restaurant_instance
                ).count() != len(restaurants_ids):
                return Response(
                    {
                        'message': 'Invalid Restuarant Branches ID Present'
                    }, status=status.HTTP_400_BAD_REQUEST)
            if len(city_ids) > 0 and RestaurantBranches.objects.filter(
                city__in=city_ids
                ).count() <= len(city_ids):
                return Response(
                    {
                        'message': 'Invalid City ID Present'
                    }, status=status.HTTP_400_BAD_REQUEST)
            if len(city_ids) > 0:
                # Assingn Voucher to all the restuarants branches in that city
                restaurants_in_city = RestaurantBranches.objects.filter(
                    city__in=city_ids,
                    restaurant=restaurant_instance
                )
                for restaurant_branch in restaurants_in_city:
                    VoucherRestaurantMap.objects.create(
                        voucher=voucher_obj, restaurant_branch=restaurant_branch)
            elif is_global:
                # Assign Voucher to all the restuarants branches
                pass
            elif not is_global and len(city_ids) <= 0 and len(restaurants_ids) > 0:
                # Assign Vocher to that Particular Restaurants
                for res_id in restaurants_ids:
                    VoucherRestaurantMap.objects.create(
                        voucher=voucher_obj,
                        restaurant_branch=RestaurantBranches.objects.get(pk=res_id)
                    )
                pass
            else:
                return Response(
                    {
                        'message': 'Invalid Request'
                    }, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VoucherCustomerBuyView(APIView):
    '''
    Customer Voucher Buy API
    '''

    def post(self, request, *args, **kwargs):

        customer_id = request.POST.get('customer_id')
        voucher_id = request.POST.get('voucher_id')

        try:
            voucher = Vouchers.objects.get(id=voucher_id)
            customer = Customers.objects.get(id=customer_id)
        except (Vouchers.DoesNotExist, Customers.DoesNotExist):
            return Response(
                {
                    "error": "Voucher or Customer not found"
                }, status=status.HTTP_404_NOT_FOUND
            )
        
        # Payment Plaform Integration code can be written here

        # Assinging Voucher to the Customer here
        voucher_transaction = VoucherHistory.objects.create(
            voucher_id=voucher,
            customer=customer
        )
        # Adding Voucher value to the wallet
        CustomerWallet.objects.create(
            value = voucher.get_price,
            medium = 'voucher',
            voucher = voucher.id
        )
        return Response(model_to_dict(voucher_transaction), status=status.HTTP_201_CREATED)

class VoucherCustomerRedeemView(APIView):

    def post(self, request, *args, **kwargs):

        customer_id = request.POST.get('customer_id')
        voucher_id = request.POST.get('voucher_id')
        amount = request.POST.get('amount', 0)

        try:
            voucher = Vouchers.objects.get(id=voucher_id)
            customer = Customers.objects.get(id=customer_id)
        except (Vouchers.DoesNotExist, Customers.DoesNotExist):
            return Response(
                {
                    "error": "Voucher or Customer not found"
                }, status=status.HTTP_404_NOT_FOUND
            )
        amount = int(amount)
        if not amount or amount <= 0:
            return Response(
                {
                    "error": "Enter Valid Amount"
                }, status=status.HTTP_400_BAD_REQUEST
            ) 
        
        voucher_transaction = VoucherHistory.objects.filter(
            voucher_id=voucher, customer=customer, redeemed=False)
        if len(voucher_transaction) > 0:
            voucher_transaction = voucher_transaction[0]
        else:
            return Response(
                {
                    "error": "Invalid Voucher"
                }, status=status.HTTP_409_CONFLICT
            
            )
        if voucher_transaction.redeemed:
            return Response(
                {
                    "error": "Voucher already redeemed"
                }, status=status.HTTP_409_CONFLICT
            
            )
        
        # Voucher should be redeemed
        voucher_transaction.redeemed = True
        voucher_transaction.redeemed_at = datetime.now()
        voucher_transaction.save()
        # Customer Wallet Instance
        customer_wallet = CustomerWallet.objects.filter(
            voucher=voucher_id, customer=customer, redeemed=False)
        if len(customer_wallet) <= 0:
            return Response(
                {
                    "error": "Invalid Transaction"
                }, status=status.HTTP_406_NOT_ACCEPTABLE
            
            )
        else:
            customer_wallet = customer_wallet[0]
        if amount == voucher.get_price:
            # Updating Wallet
            customer_wallet.redeemed = True
            customer_wallet.save()
        elif amount < voucher.get_price:
            # Vocher should be redeemed and balance should be added to wallet
            balance = voucher.get_price - amount
            # Updating Wallet
            customer_wallet.redeemed = True
            customer_wallet.save()
            # Adjusting the balance here
            CustomerWallet.objects.create(
                value = balance,
                medium = 'balance_adjusting',
                voucher = voucher.id
            )
        elif amount > voucher.get_price:
            # Outstanding balance should be ignored and voucher should be redeemed
            customer_wallet.redeemed = True
            customer_wallet.save()
            # Voucher Already redeemed
            pass

        return Response(
            {
                "message": "Voucher Redeemed Successfully"
            }, status=status.HTTP_200_OK)


