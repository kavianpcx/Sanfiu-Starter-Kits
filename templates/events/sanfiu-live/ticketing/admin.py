from django.contrib import admin

from .models import Booking, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title", "category", "city", "starts_at", "ticket_price",
        "tickets_sold", "capacity", "is_published",
    )
    list_filter = ("category", "city", "is_published", "starts_at")
    list_editable = ("ticket_price", "capacity", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "venue", "city", "summary")
    readonly_fields = ("tickets_sold", "created_at")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "public_id", "event", "attendee_name", "email", "quantity", "total", "created_at",
    )
    list_filter = ("event", "created_at")
    search_fields = ("public_id", "attendee_name", "email", "phone")
    readonly_fields = (
        "public_id", "event", "attendee_name", "email", "phone", "quantity", "total", "created_at",
    )
    fields = readonly_fields
