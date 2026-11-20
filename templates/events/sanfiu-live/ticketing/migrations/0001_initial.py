import uuid

from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("slug", models.SlugField(max_length=170, unique=True)),
                ("category", models.CharField(choices=[("music", "Music & nightlife"), ("ideas", "Talks & ideas"), ("art", "Art & culture"), ("food", "Food & drink"), ("outdoors", "Outdoors")], max_length=24)),
                ("summary", models.CharField(max_length=220)),
                ("description", models.TextField(blank=True)),
                ("venue", models.CharField(max_length=140)),
                ("city", models.CharField(max_length=80)),
                ("starts_at", models.DateTimeField()),
                ("ends_at", models.DateTimeField()),
                ("ticket_price", models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ("capacity", models.PositiveIntegerField(default=100)),
                ("tickets_sold", models.PositiveIntegerField(default=0)),
                ("image_url", models.URLField(blank=True, max_length=500)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["starts_at"]},
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("public_id", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("attendee_name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=32)),
                ("quantity", models.PositiveSmallIntegerField()),
                ("total", models.DecimalField(decimal_places=2, max_digits=9)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("event", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="bookings", to="ticketing.event")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
