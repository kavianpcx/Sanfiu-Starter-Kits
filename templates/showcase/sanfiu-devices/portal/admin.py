from django.contrib import admin
from .models import Device,Inquiry
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
 list_display=("title","category","price","is_featured","is_published")
 list_filter=("category","is_featured","is_published")
 list_editable=("price","is_featured","is_published")
 prepopulated_fields={"slug":("title",)}
 search_fields=("title","tagline","description")
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
 list_display=("device","name","email","status","created_at")
 list_filter=("status","device","created_at")
 list_editable=("status",)
 search_fields=("name","email","phone","device__title","message")
 readonly_fields=("device","name","email","phone","message","created_at")
