from decimal import Decimal

from django.core.management.base import BaseCommand

from catalog.models import Category, Product


PRODUCTS = [
    {
        "category": "Audio",
        "category_slug": "audio",
        "name": "Studio One Headphones",
        "slug": "studio-one-headphones",
        "summary": "Quiet detail. All-day comfort.",
        "description": "Over-ear wireless headphones with soft memory-foam cushions and clear, balanced sound.",
        "price": "189.00",
        "compare_at_price": "219.00",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1000&q=85",
        "stock": 18,
        "is_featured": True,
    },
    {
        "category": "Watches",
        "category_slug": "watches",
        "name": "Form Watch 02",
        "slug": "form-watch-02",
        "summary": "A clean face for every day.",
        "description": "A minimal stainless-steel watch with a lightweight case and a comfortable everyday strap.",
        "price": "145.00",
        "compare_at_price": None,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1000&q=85",
        "stock": 11,
        "is_featured": True,
    },
    {
        "category": "Audio",
        "category_slug": "audio",
        "name": "Arc Portable Speaker",
        "slug": "arc-portable-speaker",
        "summary": "Room-filling sound, ready to go.",
        "description": "A compact Bluetooth speaker with a fabric finish, warm sound, and a full-day battery.",
        "price": "98.00",
        "compare_at_price": None,
        "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=1000&q=85",
        "stock": 24,
        "is_featured": True,
    },
    {
        "category": "Carry",
        "category_slug": "carry",
        "name": "Everyday Pack",
        "slug": "everyday-pack",
        "summary": "A lighter way to carry more.",
        "description": "A durable everyday backpack with a padded laptop sleeve and thoughtful pocket layout.",
        "price": "112.00",
        "compare_at_price": "135.00",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1000&q=85",
        "stock": 9,
        "is_featured": False,
    },
    {
        "category": "Home",
        "category_slug": "home",
        "name": "Halo Table Light",
        "slug": "halo-table-light",
        "summary": "A softer glow for slow evenings.",
        "description": "A compact sculptural table lamp with a warm, diffused glow for desks and bedside tables.",
        "price": "76.00",
        "compare_at_price": None,
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1000&q=85",
        "stock": 14,
        "is_featured": False,
    },
    {
        "category": "Photography",
        "category_slug": "photography",
        "name": "Pocket Camera M2",
        "slug": "pocket-camera-m2",
        "summary": "Small camera. Big weekend energy.",
        "description": "A pocketable digital camera for everyday snapshots, travel, and everything in between.",
        "price": "329.00",
        "compare_at_price": None,
        "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=1000&q=85",
        "stock": 5,
        "is_featured": True,
    },
]


class Command(BaseCommand):
    help = "Create or update the sample categories and products."

    def handle(self, *args, **options):
        for item in PRODUCTS:
            category, _ = Category.objects.get_or_create(
                slug=item["category_slug"], defaults={"name": item["category"]}
            )
            defaults = {
                "category": category,
                "summary": item["summary"],
                "description": item["description"],
                "price": Decimal(item["price"]),
                "compare_at_price": (
                    Decimal(item["compare_at_price"])
                    if item["compare_at_price"]
                    else None
                ),
                "image_url": item["image_url"],
                "is_featured": item["is_featured"],
                "is_active": True,
            }
            product, created = Product.objects.get_or_create(
                slug=item["slug"], defaults={"name": item["name"], "stock": item["stock"], **defaults}
            )
            if not created:
                for field, value in {"name": item["name"], **defaults}.items():
                    setattr(product, field, value)
                product.save(update_fields=["name", *defaults.keys()])
        self.stdout.write(self.style.SUCCESS("Sample products are ready."))
