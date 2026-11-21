from django.db.models import Q
from django.shortcuts import get_object_or_404,render
from .models import WeatherCity

def weather_home(request):
 cities=WeatherCity.objects.filter(is_published=True).prefetch_related("forecasts")
 q=request.GET.get("q","").strip()
 if q:cities=cities.filter(Q(name__icontains=q)|Q(region__icontains=q))
 return render(request,"portal/weather_home.html",{"cities":cities,"featured_city":cities.filter(is_featured=True).first(),"query":q})

def city_detail(request,slug):
 city=get_object_or_404(WeatherCity.objects.prefetch_related("forecasts"),slug=slug,is_published=True)
 return render(request,"portal/city_detail.html",{"city":city,"forecasts":city.forecasts.all()})
