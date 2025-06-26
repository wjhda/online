import pytest
from rest_framework.test import APIClient
from .factories import ProductFactory
from django.core.cache import cache
from products.models import Product
from order.models import OrderItem


@pytest.fixture(scope="module")
def setup_product(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        Product.objects.filter(id=1).delete()
        product = ProductFactory(id=1, name='iPhone', stock=2, price=100)
        return product


@pytest.mark.django_db
@pytest.mark.parametrize("dummy", range(10))
def test_high_concurrent_order(dummy, setup_product, request):
    """
    测试多个请求并发下单同一个商品（product_id=1）
    """
    product = setup_product
    product_id = product.id

    if dummy == 0:
        # 第一次清理缓存
        cache.delete(f"stock_{product_id}")
        cache.delete(f"lock_{product_id}")

    client = APIClient()

    request_data = {
        "order_items": [
            {
                "product_id": product.id,
                "quantity": 1
            }
        ]
    }

    response = client.post("/api/order/order-info/", data=request_data, format="json")

    print(f"[{dummy}] Status Code: {response.status_code}, Body: {response.content.decode('utf-8', errors='ignore')}")

    if dummy == 9:
        product = setup_product
        sold_count = OrderItem.objects.filter(product=product).count()
        print(f"已售出 {sold_count} 件商品, 库存上限: {product.stock}")
        assert sold_count <= product.stock, \
            f"发生超卖！已售出 {sold_count}，库存只有 {product.stock}"
    assert response.status_code in [201, 400]

