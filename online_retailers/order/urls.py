from django.urls import path
from .views import OrderView

urlpatterns = [
    path('order-info/', OrderView.as_view(), name='order-info'),
]