from zoneinfo import ZoneInfo
from django.db.models import Q
from django.shortcuts import get_object_or_404,render
from django.utils import timezone
from .models import ClockCity

def clock_home(request):
 cities=ClockCity.objects.filter(is_active=True)
 q=request.GET.get("q","").strip()
 if q:cities=cities.filter(Q(name__icontains=q)|Q(region__icontains=q)|Q(timezone_name__icontains=q))
 now=timezone.now()
 clocks=[{"city":city,"local_time":now.astimezone(ZoneInfo(city.timezone_name))} for city in cities]
 return render(request,"portal/clock_home.html",{"clocks":clocks,"query":q,"server_now":now})

def clock_city(request,slug):
 city=get_object_or_404(ClockCity,is_active=True,slug=slug)
 now=timezone.now()
 return render(request,"portal/clock_city.html",{"city":city,"local_time":now.astimezone(ZoneInfo(city.timezone_name)),"server_now":now})
