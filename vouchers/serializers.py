from rest_framework import serializers
from vouchers.models import Vouchers, VoucherHistory

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vouchers
        fields = '__all__'
    
    def validate(self, attrs):
        if attrs.get('get_price') > attrs.get('buy_price') * 2:
            raise serializers.ValidationError(
                "Get price cannot be greater than double the buy price.")
        return attrs

class CustomerVoucherSerializer(serializers.ModelSerializer):
    voucher_id = VoucherSerializer()
    class Meta:
        model = VoucherHistory
        fields = '__all__'