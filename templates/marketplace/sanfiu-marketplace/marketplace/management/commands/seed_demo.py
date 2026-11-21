from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from marketplace.models import Category, Product, Seller


PRODUCTS = [
    {
        "category": "Audio", "category_slug": "audio",
        "seller_name": "North Collective", "seller_slug": "north-collective", "seller_user": "demo-north-collective",
        "name": "Studio One Headphones", "slug": "studio-one-headphones",
        "summary": "Quiet detail. All-day comfort.",
        "description": "Over-ear wireless headphones with soft memory-foam cushions and clear, balanced sound.",
        "price": "189.00", "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1000&q=85",
        "stock": 18, "is_featured": True,
    },
    {
        "category": "Carry", "category_slug": "carry",
        "seller_name": "Field Supply", "seller_slug": "field-supply", "seller_user": "demo-field-supply",
        "name": "Everyday Pack", "slug": "everyday-pack",
        "summary": "A lighter way to carry more.",
        "description": "A durable everyday backpack with a padded laptop sleeve and thoughtful pocket layout.",
        "price": "112.00", "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1000&q=85",
        "stock": 9, "is_featured": True,
    },
    {
        "category": "Home", "category_slug": "home",
        "seller_name": "Field Supply", "seller_slug": "field-supply", "seller_user": "demo-field-supply",
        "name": "Halo Table Light", "slug": "halo-table-light",
        "summary": "A softer glow for slow evenings.",
        "description": "A compact sculptural table lamp with a warm, diffused glow for desks and bedside tables.",
        "price": "76.00", "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1000&q=85",
        "stock": 14, "is_featured": False,
    },
    {
        "category": "Audio", "category_slug": "audio",
        "seller_name": "North Collective", "seller_slug": "north-collective", "seller_user": "demo-north-collective",
        "name": "Arc Portable Speaker", "slug": "arc-portable-speaker",
        "summary": "Room-filling sound, ready to go.",
        "description": "A compact Bluetooth speaker with a fabric finish, warm sound, and a full-day battery.",
        "price": "98.00", "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=1000&q=85",
        "stock": 24, "is_featured": False,
    },
]


class Command(BaseCommand):
    help = "Create or update demo sellers, categories, and products."

    def handle(self, *args, **options):
        User = get_user_model()
        seller_cache = {}
        for item in PRODUCTS:
            username = item["seller_user"]
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": f"{username}@example.invalid", "is_active": False},
            )
            if created:
                user.set_unusable_password()
                user.save(update_fields=["password"])
            seller, _ = Seller.objects.get_or_create(
                user=user,
                defaults={
                    "store_name": item["seller_name"],
                    "slug": item["seller_slug"],
                    "description": "A demo partner shop. Replace this profile with your own seller application.",
                    "review_status": Seller.ReviewStatus.APPROVED,
                },
            )
            seller_cache[item["seller_slug"]] = seller

            category, _ = Category.objects.get_or_create(
                slug=item["category_slug"], defaults={"name": item["category"]}
            )
            defaults = {
                    "seller": seller_cache[item["seller_slug"]],
                    "category": category,
                    "name": item["name"],
                    "summary": item["summary"],
                    "description": item["description"],
                    "price": Decimal(item["price"]),
                    "image_url": item["image_url"],
                    "is_featured": item["is_featured"],
                    "is_active": True,
            }
            product, created = Product.objects.get_or_create(
                slug=item["slug"], defaults={"stock": item["stock"], **defaults}
            )
            if not created:
                for field, value in defaults.items():
                    setattr(product, field, value)
                product.save(update_fields=list(defaults))
        self.stdout.write(self.style.SUCCESS("Demo marketplace data is ready."))
