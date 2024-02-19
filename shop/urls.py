from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('shop/<int:pk>/', views.product_detail, name='product-detail'),
]
