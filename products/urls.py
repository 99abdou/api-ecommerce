from django.urls import path
from .views import (
    CategoryListCreateView,
    ProductListCreateView,
    CurrentCartView,
    AddCartItemView,
    CartValidateView,
    DeleteProductView,
    RemoveCartItemView,
    ProductListSearchView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('cart/', CurrentCartView.as_view(), name='cart-detail'),
    path('cart/add/', AddCartItemView.as_view(), name='cart-add-item'),
    path('cart/validate/', CartValidateView.as_view(), name='cart-validate'),
    path('products/delete/<int:pk>/', DeleteProductView.as_view(), name='product-delete'),
    path('cart/remove/<int:product_id>/', RemoveCartItemView.as_view(), name='cart-remove-item'),
    path('products/search/', ProductListSearchView.as_view(), name='product-search'),
]
