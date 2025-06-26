from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)
    name = serializers.CharField(max_length=20, required=False)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    stock = serializers.IntegerField(required=False)

    def validate(self, attrs):
        if not self.instance:  # post请求处理
            stock = attrs.get('stock')
            price = attrs.get('price')
            if stock < 0 or price < 0:
                raise serializers.ValidationError('库存和价格不能小于0')
        return attrs

    class Meta:
        model = Product
        fields = '__all__'

