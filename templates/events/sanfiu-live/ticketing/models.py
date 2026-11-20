import uuid

from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Event(models.Model):
    CATEGORY_CHOICES = [
        ("music", "Music & nightlife"),
        ("ideas", "Talks & ideas"),
        ("art", "Art & culture"),
        ("food", "Food & drink"),
        ("outdoors", "Outdoors"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    category = models.CharField(max_length=24, choices=CATEGORY_CHOICES)
    summary = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    venue = models.CharField(max_length=140)
    city = models.CharField(max_length=80)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    capacity = models.PositiveIntegerField(default=100)
    tickets_sold = models.PositiveIntegerField(default=0)
    image_url = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["starts_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"slug": self.slug})

    @property
    def seats_left(self):
        return max(self.capacity - self.tickets_sold, 0)

    @property
    def sold_out(self):
        return self.seats_left == 0


class Booking(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name="bookings")
    attendee_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    quantity = models.PositiveSmallIntegerField()
    total = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event.title} · {self.attendee_name}"
