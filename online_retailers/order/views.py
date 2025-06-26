"""
当前代码路径下 执行以下命令 测试是否出现超卖情况
pytest test_order.py -v --ds=online_retailers.settings -n 4 --html=report.html --self-contained-html
"""

import time

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
            with transaction.atomic():
                now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                order = Order.objects.create(order_number=now)

                for item in order_items:
                    product_id = item.get('product_id')
                    quantity = item.get('quantity')

                    if not product_id or not quantity or quantity <= 0:
                        raise ValidationError("商品ID错误或商品数量不合法")

                    lock_key = f"lock_{product_id}"

                    for i in range(5):  # 最多重复5次 防止所有请求都拿不到锁的情况
                        if not cache.add(lock_key, '1', timeout=5):
                            time.sleep(0.5)
                            continue

                        try:
                            # 只有获取到锁的线程才能继续执行
                            stock = cache.get(f"stock_{product_id}")
                            if stock is None:
                                product = Product.objects.select_for_update().get(id=product_id)
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
                        except Exception as e:
                            logger.error(e)
                            raise
                        finally:
                            cache.delete(lock_key)
                        break
                    else:
                        raise ValidationError("请求超时，请稍后重试")

                return {'order_number': order.order_number}
        except ValidationError as e:
            return {'error': str(e)}

    def post(self, request):
        # 当用户进行商品下单时 前端 传入商品的id 和 数量
        try:
            order_items = request.data.get('order_items', [])
            result = self.apply_order(order_items)
            if 'error' in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response({'error': "服务器错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
