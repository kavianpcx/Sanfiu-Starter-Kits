from django.contrib import admin
from .models import Event,SellerProfile,TicketListing,TicketOrder,TicketOrderItem

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
 list_display=("title","category","city","starts_at","is_published","is_featured")
 list_filter=("category","city","is_published")
 list_editable=("is_published","is_featured")
 prepopulated_fields={"slug":("title",)}
 search_fields=("title","venue","city")

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
 list_display=("display_name","user","is_approved","joined_at")
 list_filter=("is_approved",)
 list_editable=("is_approved",)
 search_fields=("display_name","user__username","user__email")

@admin.register(TicketListing)
class TicketListingAdmin(admin.ModelAdmin):
 list_display=("event","seller","section","price","quantity_available","is_published")
 list_filter=("section","is_published","event")
 list_editable=("is_published",)
 search_fields=("event__title","seller__display_name","details")

class TicketOrderItemInline(admin.TabularInline): model=TicketOrderItem; extra=0; readonly_fields=("listing","quantity","unit_price")
@admin.register(TicketOrder)
class TicketOrderAdmin(admin.ModelAdmin):
 list_display=("public_id","buyer_name","buyer_email","buyer","total","status","created_at")
 list_filter=("status","created_at")
 search_fields=("public_id","buyer_name","buyer_email")
 readonly_fields=("public_id","buyer_name","buyer_email","total","created_at")
 inlines=[TicketOrderItemInline]
