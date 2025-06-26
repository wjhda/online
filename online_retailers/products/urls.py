from django.urls import path
from .views import ProductView

urlpatterns = [
    path('product-info/', ProductView.as_view(), name='product-info'),
]