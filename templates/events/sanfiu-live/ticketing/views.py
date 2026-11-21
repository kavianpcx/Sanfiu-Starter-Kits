from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import BookingForm
from .models import Booking, Event


def event_list(request):
    events = Event.objects.filter(is_published=True, starts_at__gte=timezone.now())
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    if query:
        events = events.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(venue__icontains=query)
            | Q(city__icontains=query)
        )
    if category in dict(Event.CATEGORY_CHOICES):
        events = events.filter(category=category)
    featured = events.filter(is_featured=True).first()
    return render(
        request,
        "ticketing/event_list.html",
        {"events": events, "featured_event": featured, "query": query, "selected_category": category},
    )


def event_detail(request, slug):
    event = get_object_or_404(Event.objects.filter(is_published=True), slug=slug)
    return render(request, "ticketing/event_detail.html", {"event": event, "form": BookingForm()})


@require_POST
def book_event(request, slug):
    event = get_object_or_404(Event.objects.filter(is_published=True), slug=slug)
    form = BookingForm(request.POST)
    if form.is_valid():
        with transaction.atomic():
            event = Event.objects.select_for_update().get(pk=event.pk)
            quantity = form.cleaned_data["quantity"]
            if event.starts_at <= timezone.now():
                messages.error(request, "Booking is closed for this event.")
                return redirect(event.get_absolute_url())
            if event.seats_left < quantity:
                messages.error(request, "There are not enough tickets left for that quantity.")
                return redirect(event.get_absolute_url())
            booking = Booking.objects.create(
                event=event,
                attendee_name=form.cleaned_data["attendee_name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                quantity=quantity,
                total=event.ticket_price * quantity,
            )
            event.tickets_sold += quantity
            event.save(update_fields=["tickets_sold"])
        messages.success(request, "Your ticket reservation is recorded.")
        return redirect("booking_confirmation", public_id=booking.public_id)
    return render(request, "ticketing/event_detail.html", {"event": event, "form": form})


def booking_confirmation(request, public_id):
    booking = get_object_or_404(Booking.objects.select_related("event"), public_id=public_id)
    return render(request, "ticketing/booking_confirmation.html", {"booking": booking})
