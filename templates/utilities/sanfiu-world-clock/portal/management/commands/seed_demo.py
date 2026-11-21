from django.core.management.base import BaseCommand
from portal.models import ClockCity
CITIES=[("New York","United States","new-york","America/New_York",True),("London","United Kingdom","london","Europe/London",True),("Tehran","Iran","tehran","Asia/Tehran",True),("Tokyo","Japan","tokyo","Asia/Tokyo",False),("Sydney","Australia","sydney","Australia/Sydney",False),("Reykjavik","Iceland","reykjavik","Atlantic/Reykjavik",False)]
class Command(BaseCommand):
 help="Create or update sample world-clock locations."
 def handle(self,*args,**options):
  for index,(name,region,slug,zone,featured) in enumerate(CITIES):
   ClockCity.objects.update_or_create(slug=slug,defaults={"name":name,"region":region,"timezone_name":zone,"is_featured":featured,"is_active":True,"sort_order":index})
  self.stdout.write(self.style.SUCCESS("Sample clock cities are ready."))
