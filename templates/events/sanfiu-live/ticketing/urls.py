from django.urls import path

from . import views

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
    path("events/<slug:slug>/book/", views.book_event, name="book_event"),
    path("bookings/<uuid:public_id>/", views.booking_confirmation, name="booking_confirmation"),
]
