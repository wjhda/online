import factory
from products.models import Product
from django.db.models.signals import post_save

@factory.django.mute_signals(post_save)
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"商品{n}")
    stock = 100