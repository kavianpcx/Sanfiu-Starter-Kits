from django.urls import path

from . import views

urlpatterns = [
    path("", views.storefront, name="storefront"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/<uuid:public_id>/", views.order_success, name="order_success"),
]
