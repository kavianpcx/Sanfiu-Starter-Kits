from django.urls import path
from . import views
urlpatterns=[path("",views.device_list,name="device_list"),path("devices/<slug:slug>/",views.device_detail,name="device_detail"),path("inquiry/thanks/",views.inquiry_confirmation,name="inquiry_confirmation")]
