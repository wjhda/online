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

            cache_product = cache.get(product_name)
            if not cache_product:
                serializer = ProductSerializer(Product.objects.filter(name__icontains=product_name), many=True)
                cache.set(product_name, serializer.data, 60)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(cache_product, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"error: {e}")
            return Response({'error': "服务器错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

