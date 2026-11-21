from .models import ClockCity
def navigation(request):
 return {"nav_clock_cities":ClockCity.objects.filter(is_active=True)[:5]}
