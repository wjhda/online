from django.db import models
from django.core.cache import cache


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name='产品名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    description = models.TextField(verbose_name='描述')
    stock = models.PositiveIntegerField(verbose_name='库存')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache_key = f"stock_{self.id}"
        cache.set(cache_key, self.stock)

    def delete(self, *args, **kwargs):
        cache_key = f"stock_{self.id}"
        cache.delete(cache_key)
        super().delete(*args, **kwargs)
        

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_info'
        verbose_name = '产品信息表'
