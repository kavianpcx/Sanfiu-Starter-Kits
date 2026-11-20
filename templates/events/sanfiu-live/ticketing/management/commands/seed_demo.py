from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from ticketing.models import Event


EVENTS = [
    {
        "title": "After Hours: A Night of Live Jazz", "slug": "after-hours-live-jazz",
        "category": "music", "summary": "An intimate set from a new generation of jazz musicians.",
        "description": "Settle in for a late-night performance, a good drink, and a room full of people who love live music.",
        "venue": "The Foundry Room", "city": "Brooklyn, NY", "days": 12, "hour": 20,
        "ticket_price": "28.00", "capacity": 120,
        "image_url": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?auto=format&fit=crop&w=1200&q=85",
        "is_featured": True,
    },
    {
        "title": "Small Ideas, Big Futures", "slug": "small-ideas-big-futures",
        "category": "ideas", "summary": "A one-day gathering for people building what comes next.",
        "description": "Short talks, shared lunch, and open conversation about making better products and communities.",
        "venue": "Pier 17 Studio", "city": "New York, NY", "days": 20, "hour": 10,
        "ticket_price": "64.00", "capacity": 180,
        "image_url": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?auto=format&fit=crop&w=1200&q=85",
        "is_featured": True,
    },
    {
        "title": "Sunday Table: Seasonal Supper Club", "slug": "sunday-table-supper-club",
        "category": "food", "summary": "A shared menu built around what is in season.",
        "description": "Meet new people around a long table for a relaxed, chef-led seasonal dinner.",
        "venue": "June House", "city": "Queens, NY", "days": 27, "hour": 18,
        "ticket_price": "52.00", "capacity": 36,
        "image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=1200&q=85",
        "is_featured": False,
    },
    {
        "title": "Open Studio: Print & Paper", "slug": "open-studio-print-paper",
        "category": "art", "summary": "A hands-on afternoon with local printmakers.",
        "description": "Try a few simple printmaking techniques and leave with something you made yourself.",
        "venue": "West Works Studio", "city": "Brooklyn, NY", "days": 34, "hour": 13,
        "ticket_price": "18.00", "capacity": 24,
        "image_url": "https://images.unsplash.com/photo-1531058020387-3be344556be6?auto=format&fit=crop&w=1200&q=85",
        "is_featured": False,
    },
    {
        "title": "Sunset Walk & Picnic", "slug": "sunset-walk-picnic",
        "category": "outdoors", "summary": "An easy-paced walk ending with a picnic by the water.",
        "description": "Bring a friend, wear comfortable shoes, and enjoy a guided stroll before golden hour.",
        "venue": "Domino Park entrance", "city": "Brooklyn, NY", "days": 41, "hour": 17,
        "ticket_price": "12.00", "capacity": 40,
        "image_url": "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=1200&q=85",
        "is_featured": False,
    },
]


class Command(BaseCommand):
    help = "Create or update the sample events."

    def handle(self, *args, **options):
        now = timezone.now()
        for item in EVENTS:
            starts_at = now + timedelta(days=item["days"])
            starts_at = starts_at.replace(hour=item["hour"], minute=0, second=0, microsecond=0)
            defaults = {
                "title": item["title"], "category": item["category"],
                "summary": item["summary"], "description": item["description"],
                "venue": item["venue"], "city": item["city"], "starts_at": starts_at,
                "ends_at": starts_at + timedelta(hours=3),
                "ticket_price": Decimal(item["ticket_price"]), "capacity": item["capacity"],
                "image_url": item["image_url"], "is_featured": item["is_featured"],
                "is_published": True,
            }
            Event.objects.update_or_create(slug=item["slug"], defaults=defaults)
        self.stdout.write(self.style.SUCCESS("Sample events are ready."))
