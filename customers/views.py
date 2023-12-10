# views.py
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from customers.models import Customers, CustomerWallet

from .serializers import CustomerWalletSerializer

# Create your views here.
class ListCustomerWallet(APIView):
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
        queryset = CustomerWallet.objects.filter(customer=customer, redeemed=False)
        serializer = CustomerWalletSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)