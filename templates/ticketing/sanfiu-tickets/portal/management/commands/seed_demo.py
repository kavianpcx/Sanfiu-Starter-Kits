from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from portal.models import Event, SellerProfile, TicketListing


SHOWS = [
    {
        "title": "The Last Comet",
        "slug": "the-last-comet",
        "category": "movies",
        "summary": "A night-shift astronomer catches a signal at the edge of the solar system.",
        "description": "A fictional sample film and screening. Replace its details, poster, cinema, and showtime with your own catalog.",
        "venue": "Orchid Cinema · Screen 4",
        "city": "Austin, TX",
        "days": 2,
        "hour": 19,
        "image_url": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1000&q=85",
        "featured": True,
        "seller": "demo_cinema_partner",
        "seller_name": "Orchid Cinema Box Office",
        "offers": [("standard", "Standard · Row G", "12.00", 48), ("premium", "Premium · centered seats", "18.00", 16)],
    },
    {
        "title": "Glass Harbor",
        "slug": "glass-harbor",
        "category": "movies",
        "summary": "A marine biologist returns to the island where her family built a lighthouse.",
        "description": "A fictional drama sample. This page represents a single upcoming showtime; add more sessions as separate entries.",
        "venue": "Northline Picture House · Screen 2",
        "city": "Chicago, IL",
        "days": 2,
        "hour": 20,
        "image_url": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&w=1000&q=85",
        "featured": False,
        "seller": "demo_cinema_partner",
        "seller_name": "Northline Box Office",
        "offers": [("standard", "Standard · Rows E–H", "11.00", 35), ("vip", "Premiere lounge", "24.00", 8)],
    },
    {
        "title": "A Map of Small Stars",
        "slug": "map-of-small-stars",
        "category": "movies",
        "summary": "Two siblings cross the desert to return a lost telescope before sunrise.",
        "description": "Fictional sample film details for the demo catalog. Edit this text and the image in Django admin.",
        "venue": "Juniper Arts Cinema · Screen 1",
        "city": "Portland, OR",
        "days": 3,
        "hour": 18,
        "image_url": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?auto=format&fit=crop&w=1000&q=85",
        "featured": False,
        "seller": "demo_cinema_partner",
        "seller_name": "Juniper Cinema Desk",
        "offers": [("standard", "Standard · Row F", "10.00", 42), ("premium", "Loveseat pair", "30.00", 6)],
    },
    {
        "title": "After the Blue Hour",
        "slug": "after-the-blue-hour",
        "category": "movies",
        "summary": "A quiet city mystery unfolds over one late-night train ride.",
        "description": "A fictional sample screening, set up to demonstrate film discovery and ticket inventory.",
        "venue": "Silver Screen IMAX · Hall 3",
        "city": "Seattle, WA",
        "days": 4,
        "hour": 21,
        "image_url": "https://images.unsplash.com/photo-1518929458119-e5bf444c30f4?auto=format&fit=crop&w=1000&q=85",
        "featured": False,
        "seller": "demo_cinema_partner",
        "seller_name": "Silver Screen Tickets",
        "offers": [("standard", "Standard · Rows C–F", "14.00", 52), ("vip", "IMAX premium", "22.00", 12)],
    },
    {
        "title": "Bluewater Adventure Park",
        "slug": "bluewater-adventure-park",
        "category": "waterparks",
        "summary": "A full day of wave pools, lazy rivers, and family slides.",
        "description": "Sample day passes for a fictional water park. Set real dates, capacity, terms, and pricing before launch.",
        "venue": "Bluewater Adventure Park",
        "city": "San Diego, CA",
        "days": 5,
        "hour": 10,
        "image_url": "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?auto=format&fit=crop&w=1000&q=85",
        "featured": False,
        "seller": "demo_waterpark_partner",
        "seller_name": "Bluewater Guest Services",
        "offers": [("day_pass", "All-day admission", "39.00", 80), ("family", "Family day pass · 4 guests", "128.00", 15)],
    },
    {
        "title": "Cascade Lagoon Family Day",
        "slug": "cascade-lagoon-family-day",
        "category": "waterparks",
        "summary": "Reserve a sunny day at a riverside water-play park.",
        "description": "Sample dated admission passes. Connect a payment provider and enforce real venue capacity for production use.",
        "venue": "Cascade Lagoon",
        "city": "Portland, OR",
        "days": 6,
        "hour": 11,
        "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1000&q=85",
        "featured": False,
        "seller": "demo_waterpark_partner",
        "seller_name": "Cascade Lagoon Tickets",
        "offers": [("day_pass", "General day pass", "32.00", 65), ("vip", "Cabana + day pass", "96.00", 4)],
    },
]


class Command(BaseCommand):
    help = "Create sample cinema showtimes and water-park tickets."

    def handle(self, *args, **options):
        user_model = get_user_model()
        sellers = {}
        for item in SHOWS:
            if item["seller"] not in sellers:
                user, _ = user_model.objects.get_or_create(
                    username=item["seller"],
                    defaults={"email": "seller@example.com"},
                )
                if not user.has_usable_password():
                    user.set_unusable_password()
                    user.save(update_fields=["password"])
                sellers[item["seller"]], _ = SellerProfile.objects.update_or_create(
                    user=user,
                    defaults={"display_name": item["seller_name"], "is_approved": True},
                )

        now = timezone.localtime()
        for item in SHOWS:
            starts = (now + timedelta(days=item["days"])).replace(
                hour=item["hour"], minute=0, second=0, microsecond=0
            )
            event, _ = Event.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "category": item["category"],
                    "summary": item["summary"],
                    "description": item["description"],
                    "venue": item["venue"],
                    "city": item["city"],
                    "starts_at": starts,
                    "image_url": item["image_url"],
                    "is_featured": item["featured"],
                    "is_published": True,
                },
            )
            seller = sellers[item["seller"]]
            for section, details, price, quantity in item["offers"]:
                TicketListing.objects.update_or_create(
                    event=event,
                    seller=seller,
                    section=section,
                    defaults={
                        "details": details,
                        "price": Decimal(price),
                        "quantity_available": quantity,
                        "is_published": True,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS("Sample film screenings and water-park passes are ready.")
        )
