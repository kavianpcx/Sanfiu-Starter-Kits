from .models import WeatherCity
def navigation(request):
 return {"nav_cities":WeatherCity.objects.filter(is_published=True)[:5]}
