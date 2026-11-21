from datetime import timedelta
from django.db.models import Q
from django.shortcuts import get_object_or_404,render
from django.utils import timezone
from .models import WeatherCity

def weather_home(request):
 cities=WeatherCity.objects.filter(is_published=True).prefetch_related("forecasts","hourly_forecasts")
 q=request.GET.get("q","").strip()
 featured_city=WeatherCity.objects.filter(is_published=True,is_featured=True).prefetch_related("forecasts","hourly_forecasts").first()
 if q:cities=cities.filter(Q(name__icontains=q)|Q(region__icontains=q))
 hourly=featured_city.hourly_forecasts.filter(forecast_at__gte=timezone.now()-timedelta(minutes=30))[:8] if featured_city else []
 return render(request,"portal/weather_home.html",{"cities":cities,"featured_city":featured_city,"featured_hours":hourly,"featured_forecasts":featured_city.forecasts.all()[:5] if featured_city else [],"query":q})

def city_detail(request,slug):
 city=get_object_or_404(WeatherCity.objects.prefetch_related("forecasts","hourly_forecasts"),slug=slug,is_published=True)
 hourly=city.hourly_forecasts.filter(forecast_at__gte=timezone.now()-timedelta(minutes=30))[:10]
 return render(request,"portal/city_detail.html",{"city":city,"forecasts":city.forecasts.all()[:10],"hourly":hourly})
