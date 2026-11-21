from zoneinfo import ZoneInfo,ZoneInfoNotFoundError
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

class ClockCity(models.Model):
 name=models.CharField(max_length=100)
 region=models.CharField(max_length=100,blank=True)
 slug=models.SlugField(max_length=120,unique=True)
 timezone_name=models.CharField(max_length=80,help_text="Use an IANA timezone name, for example America/New_York.")
 is_featured=models.BooleanField(default=False)
 is_active=models.BooleanField(default=True)
 sort_order=models.PositiveSmallIntegerField(default=0)
 class Meta:ordering=["sort_order","name"]
 def __str__(self):return f"{self.name} · {self.timezone_name}"
 def clean(self):
  try:ZoneInfo(self.timezone_name)
  except ZoneInfoNotFoundError as exc:raise ValidationError({"timezone_name":"Enter a valid IANA time zone."}) from exc
 def get_absolute_url(self):return reverse("clock_city",kwargs={"slug":self.slug})
