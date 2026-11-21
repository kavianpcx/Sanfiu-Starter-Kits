from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from portal.models import Event,SellerProfile,TicketListing

EVENTS=[
 {"title":"After Hours Jazz Session","slug":"after-hours-jazz-session","category":"music","summary":"A close-up set from a brilliant local quartet.","venue":"The Foundry Hall","city":"Brooklyn, NY","days":14,"hour":20,"image_url":"https://images.unsplash.com/photo-1511192336575-5a79af67a629?auto=format&fit=crop&w=1200&q=85","featured":True},
 {"title":"New York City FC vs. Austin","slug":"nycfc-vs-austin","category":"sports","summary":"An afternoon match with a loud home crowd.","venue":"Harbor Field","city":"New York, NY","days":19,"hour":15,"image_url":"https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1200&q=85","featured":True},
 {"title":"The Long Way Home","slug":"the-long-way-home","category":"arts","summary":"A new stage production about finding your way back.","venue":"Marlowe Theatre","city":"New York, NY","days":26,"hour":19,"image_url":"https://images.unsplash.com/photo-1503095396549-807759245b35?auto=format&fit=crop&w=1200&q=85","featured":False},
]
class Command(BaseCommand):
 help="Create or update sample events and tickets."
 def handle(self,*args,**options):
  user_model=get_user_model(); user,_=user_model.objects.get_or_create(username="demo_seller",defaults={"email":"seller@example.com"})
  if not user.has_usable_password(): user.set_unusable_password(); user.save(update_fields=["password"])
  seller,_=SellerProfile.objects.update_or_create(user=user,defaults={"display_name":"Northstar Tickets","is_approved":True})
  now=timezone.now()
  for index,item in enumerate(EVENTS):
   starts=(now+timedelta(days=item["days"])).replace(hour=item["hour"],minute=0,second=0,microsecond=0)
   event,_=Event.objects.update_or_create(slug=item["slug"],defaults={"title":item["title"],"category":item["category"],"summary":item["summary"],"description":"Browse verified-style sample listings from independent sellers. This starter does not issue a paid ticket.","venue":item["venue"],"city":item["city"],"starts_at":starts,"image_url":item["image_url"],"is_featured":item["featured"],"is_published":True})
   TicketListing.objects.update_or_create(event=event,seller=seller,section=["lower","floor","vip"][index],defaults={"details":"Sample listing · adjacent seats","price":Decimal(["48.00","72.00","55.00"][index]),"quantity_available":[4,2,3][index],"is_published":True})
  self.stdout.write(self.style.SUCCESS("Sample ticket events are ready."))
