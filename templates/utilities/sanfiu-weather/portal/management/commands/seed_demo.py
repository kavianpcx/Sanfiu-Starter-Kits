from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from portal.models import DailyForecast,WeatherCity
CITIES=[
 {"name":"San Francisco","region":"California","slug":"san-francisco","current_temp":"19","condition":"Clear skies","high":"22","low":"14","humidity":48,"wind_kph":"12","image_url":"https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=1400&q=85","featured":True,"days":[("Mostly sunny",22,14,5),("Partly cloudy",21,14,10),("Clear",23,15,0),("Breezy",20,13,15),("Mostly sunny",22,14,0)]},
 {"name":"Portland","region":"Oregon","slug":"portland","current_temp":"16","condition":"Passing clouds","high":"18","low":"11","humidity":62,"wind_kph":"9","image_url":"https://images.unsplash.com/photo-1509475826633-fed577a2c71b?auto=format&fit=crop&w=1400&q=85","featured":False,"days":[("Cloudy",18,11,20),("Light rain",16,10,65),("Partly cloudy",19,11,10),("Clear",20,12,0),("Cloudy",17,10,25)]},
 {"name":"Austin","region":"Texas","slug":"austin","current_temp":"27","condition":"Warm and bright","high":"30","low":"20","humidity":41,"wind_kph":"8","image_url":"https://images.unsplash.com/photo-1531218150217-54595bc2b934?auto=format&fit=crop&w=1400&q=85","featured":False,"days":[("Sunny",30,20,0),("Clear",31,21,0),("Mostly sunny",29,19,5),("Warm",28,20,10),("Sunny",32,21,0)]},
]
class Command(BaseCommand):
 help="Create or update clearly labeled sample weather forecasts."
 def handle(self,*args,**options):
  today=timezone.localdate()
  for item in CITIES:
   data={k:v for k,v in item.items() if k not in {"days","slug","featured"}}
   data["is_featured"]=item["featured"]
   for key in ("current_temp","high","low","wind_kph"):data[key]=Decimal(str(data[key]))
   city,_=WeatherCity.objects.update_or_create(slug=item["slug"],defaults=data)
   for offset,(condition,high,low,rain) in enumerate(item["days"]):
    DailyForecast.objects.update_or_create(city=city,forecast_date=today+timedelta(days=offset),defaults={"condition":condition,"high":Decimal(str(high)),"low":Decimal(str(low)),"precipitation_percent":rain})
  self.stdout.write(self.style.SUCCESS("Sample forecasts are ready. They are not live weather data."))
