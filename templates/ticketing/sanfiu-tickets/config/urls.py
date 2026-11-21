from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from portal import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", views.SellerLoginView.as_view(), name="login"),
    path("accounts/buyer-login/", views.BuyerLoginView.as_view(), name="buyer_login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", views.seller_signup, name="seller_signup"),
    path("accounts/buyer-signup/", views.buyer_signup, name="buyer_signup"),
    path("account/tickets/", views.buyer_account, name="buyer_account"),
    path("", include("portal.urls")),
]
