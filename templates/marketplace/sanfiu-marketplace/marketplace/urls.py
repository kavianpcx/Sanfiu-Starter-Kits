from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.storefront, name="storefront"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("stores/<slug:slug>/", views.store_page, name="store_page"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/<uuid:public_id>/", views.order_success, name="order_success"),
    path("seller/apply/", views.seller_apply, name="seller_apply"),
    path("seller/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="seller_login"),
    path("seller/logout/", auth_views.LogoutView.as_view(), name="seller_logout"),
    path("seller/", views.seller_dashboard, name="seller_dashboard"),
    path("seller/products/new/", views.seller_product_new, name="seller_product_new"),
    path("seller/products/<int:product_id>/edit/", views.seller_product_edit, name="seller_product_edit"),
    path("seller/order-items/<int:item_id>/status/", views.seller_update_fulfillment, name="seller_update_fulfillment"),
]
