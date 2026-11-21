from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models
from django.urls import reverse

class WeatherCity(models.Model):
 name=models.CharField(max_length=100)
 region=models.CharField(max_length=100,blank=True)
 slug=models.SlugField(max_length=120,unique=True)
 current_temp=models.DecimalField(max_digits=5,decimal_places=1)
 condition=models.CharField(max_length=80)
 high=models.DecimalField(max_digits=5,decimal_places=1)
 low=models.DecimalField(max_digits=5,decimal_places=1)
 humidity=models.PositiveSmallIntegerField(default=50,validators=[MinValueValidator(0),MaxValueValidator(100)])
 wind_kph=models.DecimalField(max_digits=5,decimal_places=1,default=0)
 image_url=models.URLField(max_length=500,blank=True)
 updated_at=models.DateTimeField(auto_now=True)
 is_featured=models.BooleanField(default=False)
 is_published=models.BooleanField(default=True)
 class Meta:ordering=["-is_featured","name"]
 def __str__(self):return f"{self.name}, {self.region}" if self.region else self.name
 def get_absolute_url(self):return reverse("city_detail",kwargs={"slug":self.slug})
 @property
 def weather_icon(self):return icon_for(self.condition)

def icon_for(condition):
 text=condition.lower()
 if any(word in text for word in ("rain","shower","storm")):return "🌧️"
 if "snow" in text:return "❄️"
 if "wind" in text or "breez" in text:return "💨"
 if "cloud" in text:return "⛅"
 return "☀️"

class DailyForecast(models.Model):
 city=models.ForeignKey(WeatherCity,on_delete=models.CASCADE,related_name="forecasts")
 forecast_date=models.DateField()
 condition=models.CharField(max_length=80)
 high=models.DecimalField(max_digits=5,decimal_places=1)
 low=models.DecimalField(max_digits=5,decimal_places=1)
 precipitation_percent=models.PositiveSmallIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])
 class Meta:
  ordering=["forecast_date"]
  constraints=[models.UniqueConstraint(fields=["city","forecast_date"],name="unique_weather_city_date")]
 def __str__(self):return f"{self.city} · {self.forecast_date}"
 @property
 def weather_icon(self):return icon_for(self.condition)

class HourlyForecast(models.Model):
 city=models.ForeignKey(WeatherCity,on_delete=models.CASCADE,related_name="hourly_forecasts")
 forecast_at=models.DateTimeField()
 temperature=models.DecimalField(max_digits=5,decimal_places=1)
 condition=models.CharField(max_length=80)
 precipitation_percent=models.PositiveSmallIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])
 wind_kph=models.DecimalField(max_digits=5,decimal_places=1,default=0)
 class Meta:
  ordering=["forecast_at"]
  constraints=[models.UniqueConstraint(fields=["city","forecast_at"],name="unique_weather_city_hour")]
 def __str__(self):return f"{self.city} · {self.forecast_at}"
 @property
 def weather_icon(self):return icon_for(self.condition)
