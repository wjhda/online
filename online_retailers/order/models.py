from django.db import models
from products.models import Product

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=20, verbose_name='订单编号')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.order_number

    class Meta:
        db_table = 'order'
        verbose_name = '订单'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    quantity = models.PositiveIntegerField(verbose_name='数量')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f"{self.order.order_number} -- {self.product.name} -- {self.quantity} -- {self.product.price}"

    class Meta:
        db_table = 'order_item'
        verbose_name = '订单信息'
