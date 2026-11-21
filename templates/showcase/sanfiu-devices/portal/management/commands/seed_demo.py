from decimal import Decimal
from django.core.management.base import BaseCommand
from portal.models import Device
DEVICES=[
 {"title":"Aster One Pro","slug":"aster-one-pro","category":"phone","tagline":"A little more room for big ideas.","description":"A refined everyday phone with a bright display, a versatile camera system, and long-lasting battery life. Built as an original sample catalog entry for this customizable device showcase.","price":"899.00","image_url":"https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=1400&q=85","finish":"Graphite","display":"6.3-inch OLED","processor":"Aster X4","battery":"Up to 26 hours","camera":"48 MP dual camera","storage":"256 GB","is_featured":True},
 {"title":"Aster One","slug":"aster-one","category":"phone","tagline":"Everything you need. Nothing in the way.","description":"A comfortable, capable phone for the everyday. Customize its name, specifications, prices, photos, and product story in the admin panel.","price":"649.00","image_url":"https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1400&q=85","finish":"Mist","display":"6.1-inch OLED","processor":"Aster X3","battery":"Up to 22 hours","camera":"48 MP camera","storage":"128 GB","is_featured":False},
 {"title":"Aster Book Air","slug":"aster-book-air","category":"computer","tagline":"Room to make. Space to move.","description":"A lightweight notebook for focused work, creative sessions, and everyday tasks. Replace the sample specs with your own catalog data.","price":"1199.00","image_url":"https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1400&q=85","finish":"Silver","display":"14-inch Retina-style display","processor":"Aster M3","battery":"Up to 18 hours","camera":"1080p webcam","storage":"512 GB","is_featured":False},
]
class Command(BaseCommand):
 help="Create or update sample device catalog entries."
 def handle(self,*args,**options):
  for item in DEVICES:
   data=item.copy();data["price"]=Decimal(data["price"]);data["is_published"]=True
   Device.objects.update_or_create(slug=data.pop("slug"),defaults={"slug":item["slug"],**data})
  self.stdout.write(self.style.SUCCESS("Sample devices are ready."))
