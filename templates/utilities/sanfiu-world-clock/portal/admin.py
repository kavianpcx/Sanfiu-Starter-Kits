from django.contrib import admin
from .models import ClockCity
@admin.register(ClockCity)
class ClockCityAdmin(admin.ModelAdmin):
 list_display=("name","region","timezone_name","is_featured","is_active","sort_order")
 list_filter=("is_featured","is_active")
 list_editable=("is_featured","is_active","sort_order")
 prepopulated_fields={"slug":("name",)}
 search_fields=("name","region","timezone_name")
