from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/customer_login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", views.customer_signup, name="customer_signup"),
    path("account/", views.customer_account, name="customer_account"),
    path("", views.storefront, name="storefront"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/<uuid:public_id>/", views.order_success, name="order_success"),
]
