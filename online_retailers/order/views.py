from django.db import transaction
from django.core.cache import cache
from .models import Order, OrderItem
from products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from rest_framework.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class OrderView(APIView):

    def apply_order(self, order_items):
        try:
            with transaction.atomic():  # 整个下单流程在一个事务中 防止出现空订单的问题
                now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                order = Order.objects.create(order_number=now)

                for item in order_items:
                    product_id = item.get('product_id')
                    quantity = item.get('quantity')

                    # 获取缓存中的库存
                    stock = cache.get(f"stock_{product_id}")
                    if stock is None:
                        product = Product.objects.get(id=product_id)
                        if not product:
                            raise ValidationError("商品不存在")
                        stock = product.stock
                        cache.set(f"stock_{product_id}", stock)

                    if stock < quantity:
                        raise ValidationError("库存不足")

                    product = Product.objects.select_for_update().get(id=product_id)
                    if product.stock < quantity:
                        raise ValidationError("库存不足")

                    product.stock -= quantity
                    product.save()
                    cache.set(f"stock_{product_id}", product.stock)

                    OrderItem.objects.create(order=order, product=product, quantity=quantity)

                return {'order_number': order.order_number}
        except ValidationError as e:
            return {'error': str(e)}
    def post(self, request):
        # 当用户进行商品下单时 前端 传入商品的id 和 数量
        try:
            order_items = request.data.get('order_items', [])
            print(order_items)
            result = self.apply_order(order_items)
            if 'error' in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response({'error': "服务器错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
