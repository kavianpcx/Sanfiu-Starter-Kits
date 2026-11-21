from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from portal.models import DailyForecast, HourlyForecast, WeatherCity


CITIES = [
    {
        "name": "San Francisco", "region": "California", "slug": "san-francisco",
        "current_temp": "19", "condition": "Mostly sunny", "high": "22", "low": "14",
        "humidity": 48, "wind_kph": "12",
        "image_url": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=1400&q=85",
        "featured": True,
        "days": [("Mostly sunny",22,14,5),("Partly cloudy",21,14,10),("Clear",23,15,0),("Breezy",20,13,15),("Mostly sunny",22,14,0),("Cloudy",19,13,20),("Clear",24,15,0),("Light rain",18,12,45),("Partly cloudy",20,13,10),("Sunny",23,14,0)],
        "hours": [("Clear",0,0,8),("Mostly sunny",1,0,10),("Sunny",2,0,12),("Breezy",2,0,17),("Partly cloudy",1,5,15),("Cloudy",0,10,11),("Mostly sunny",-1,5,9),("Clear",-2,0,7)],
    },
    {
        "name": "Portland", "region": "Oregon", "slug": "portland",
        "current_temp": "16", "condition": "Passing clouds", "high": "18", "low": "11",
        "humidity": 62, "wind_kph": "9",
        "image_url": "https://images.unsplash.com/photo-1509475826633-fed577a2c71b?auto=format&fit=crop&w=1400&q=85",
        "featured": False,
        "days": [("Cloudy",18,11,20),("Light rain",16,10,65),("Partly cloudy",19,11,10),("Clear",20,12,0),("Cloudy",17,10,25),("Showers",15,9,70),("Mostly cloudy",17,10,25),("Partly cloudy",19,11,10),("Clear",21,12,0),("Light rain",16,10,45)],
        "hours": [("Cloudy",0,15,7),("Passing clouds",1,10,8),("Light rain",1,45,10),("Light rain",0,60,12),("Cloudy",-1,35,9),("Cloudy",0,20,7),("Partly cloudy",1,10,6),("Clear",0,0,5)],
    },
    {
        "name": "Austin", "region": "Texas", "slug": "austin",
        "current_temp": "27", "condition": "Warm and bright", "high": "30", "low": "20",
        "humidity": 41, "wind_kph": "8",
        "image_url": "https://images.unsplash.com/photo-1531218150217-54595bc2b934?auto=format&fit=crop&w=1400&q=85",
        "featured": False,
        "days": [("Sunny",30,20,0),("Clear",31,21,0),("Mostly sunny",29,19,5),("Warm",28,20,10),("Sunny",32,21,0),("Partly cloudy",29,20,10),("Sunny",31,21,0),("Clear",32,22,0),("Breezy",28,19,0),("Sunny",30,20,0)],
        "hours": [("Sunny",0,0,7),("Sunny",1,0,9),("Mostly sunny",2,0,12),("Warm",3,0,14),("Sunny",2,0,15),("Clear",1,0,11),("Clear",0,0,9),("Clear",-1,0,7)],
    },
]


class Command(BaseCommand):
    help = "Create or update clearly labeled sample weather forecasts."

    def handle(self, *args, **options):
        today = timezone.localdate()
        first_hour = timezone.localtime().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        for item in CITIES:
            data = {key: value for key, value in item.items() if key not in {"days", "hours", "slug", "featured"}}
            data["is_featured"] = item["featured"]
            for key in ("current_temp", "high", "low", "wind_kph"):
                data[key] = Decimal(str(data[key]))
            city, _ = WeatherCity.objects.update_or_create(slug=item["slug"], defaults=data)

            for offset, (condition, high, low, rain) in enumerate(item["days"]):
                DailyForecast.objects.update_or_create(
                    city=city,
                    forecast_date=today + timedelta(days=offset),
                    defaults={
                        "condition": condition,
                        "high": Decimal(str(high)),
                        "low": Decimal(str(low)),
                        "precipitation_percent": rain,
                    },
                )

            for offset, (condition, temp_delta, rain, wind) in enumerate(item["hours"]):
                HourlyForecast.objects.update_or_create(
                    city=city,
                    forecast_at=first_hour + timedelta(hours=offset * 3),
                    defaults={
                        "condition": condition,
                        "temperature": Decimal(str(item["current_temp"])) + Decimal(str(temp_delta)),
                        "precipitation_percent": rain,
                        "wind_kph": Decimal(str(wind)),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Sample hourly and 10-day forecasts are ready. They are not live weather data."))
