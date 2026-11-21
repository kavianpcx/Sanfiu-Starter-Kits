from django.contrib import admin
from .models import DailyForecast,WeatherCity
class DailyForecastInline(admin.TabularInline):
 model=DailyForecast;extra=0
@admin.register(WeatherCity)
class WeatherCityAdmin(admin.ModelAdmin):
 list_display=("name","region","current_temp","condition","is_featured","is_published","updated_at")
 list_filter=("condition","is_featured","is_published")
 list_editable=("is_featured","is_published")
 prepopulated_fields={"slug":("name",)}
 search_fields=("name","region","condition")
 inlines=[DailyForecastInline]
@admin.register(DailyForecast)
class DailyForecastAdmin(admin.ModelAdmin):
 list_display=("city","forecast_date","condition","high","low","precipitation_percent")
 list_filter=("condition","forecast_date")
 search_fields=("city__name",)
