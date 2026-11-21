from django.urls import path
from . import views
urlpatterns=[
 path("",views.event_list,name="event_list"),
 path("events/<slug:slug>/",views.event_detail,name="event_detail"),
 path("tickets/<int:listing_id>/buy/",views.buy_ticket,name="buy_ticket"),
 path("orders/<uuid:public_id>/",views.order_confirmation,name="order_confirmation"),
 path("sell/",views.seller_dashboard,name="seller_dashboard"),
 path("sell/apply/",views.seller_signup,name="seller_signup"),
 path("sell/listings/new/",views.create_listing,name="create_listing"),
]
