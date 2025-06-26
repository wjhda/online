import time

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Product
from .serializer import ProductSerializer
import logging

logger = logging.getLogger(__name__)


class ProductView(APIView):
    def get(self, request):
        try:
            query = request.query_params
            if not query:
                return Response({'error': "请输入要查询的产品信息"}, status=status.HTTP_400_BAD_REQUEST)

            product_name = query.get('product_name')
            if not product_name:
                return Response({'error': "请输入要查询的产品名称"}, status=status.HTTP_400_BAD_REQUEST)

            # 检查缓存是否存在
            cache_product = cache.get(product_name)
            if cache_product:
                return Response(cache_product, status=status.HTTP_200_OK)

            # 缓存失效后，尝试最多3次重试
            for i in range(3):
                time.sleep(0.1)  # 短暂延迟避免瞬间冲击
                cache_product = cache.get(product_name)
                if cache_product:
                    return Response(cache_product, status=status.HTTP_200_OK)

            # 加锁防止缓存击穿
            lock_key = f"{product_name}_lock"
            if cache.add(lock_key, "1", timeout=5):  # 尝试加锁 为每个商品加上同名称的锁 保证锁的唯一性
                try:
                    # 数据库查询
                    queryset = Product.objects.filter(name__icontains=product_name)
                    serializer = ProductSerializer(queryset, many=True)

                    # 设置缓存，带随机过期时间防止雪崩 防止同一时间所有的缓存失效 多个请求同时访问数据库 这样加了随机过期时间 就不会出现多个请求都访问数据库
                    import random
                    cache_timeout = 60 + random.randint(0, 30)
                    cache.set(product_name, serializer.data, cache_timeout)

                    return Response(serializer.data, status=status.HTTP_200_OK)
                finally:
                    cache.delete(lock_key)  # 释放锁  防止出现死锁情况
            else:
                # 其他请求等待主请求加载数
                time.sleep(0.5)
                cache_product = cache.get(product_name)
                if cache_product:
                    return Response(cache_product, status=status.HTTP_200_OK)
                return Response({'error': '请稍后再试'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except Exception as e:
            logger.error(f"error: {e}")
            return Response({'error': "服务器错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
