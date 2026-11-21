from django.urls import path
from . import views
urlpatterns=[path("",views.clock_home,name="clock_home"),path("cities/<slug:slug>/",views.clock_city,name="clock_city")]
