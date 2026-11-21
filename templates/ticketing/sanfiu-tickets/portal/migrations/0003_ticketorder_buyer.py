from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("portal", "0002_cinema_and_attraction_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticketorder",
            name="buyer",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="ticket_orders", to=settings.AUTH_USER_MODEL),
        ),
    ]
