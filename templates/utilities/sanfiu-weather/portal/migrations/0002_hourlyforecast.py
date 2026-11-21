from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [("portal", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="HourlyForecast",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("forecast_at", models.DateTimeField()),
                ("temperature", models.DecimalField(decimal_places=1, max_digits=5)),
                ("condition", models.CharField(max_length=80)),
                ("precipitation_percent", models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ("wind_kph", models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ("city", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="hourly_forecasts", to="portal.weathercity")),
            ],
            options={"ordering": ["forecast_at"]},
        ),
        migrations.AddConstraint(
            model_name="hourlyforecast",
            constraint=models.UniqueConstraint(fields=("city", "forecast_at"), name="unique_weather_city_hour"),
        ),
    ]
