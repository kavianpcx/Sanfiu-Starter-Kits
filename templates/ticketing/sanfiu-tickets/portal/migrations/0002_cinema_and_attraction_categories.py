from django.db import migrations, models


def map_existing_choices(apps, schema_editor):
    Event = apps.get_model("portal", "Event")
    TicketListing = apps.get_model("portal", "TicketListing")
    Event.objects.exclude(category="other").update(category="live")
    TicketListing.objects.filter(section="general").update(section="standard")
    TicketListing.objects.filter(section__in=("floor", "lower", "upper")).update(section="premium")


class Migration(migrations.Migration):
    dependencies = [("portal", "0001_initial")]

    operations = [
        migrations.RunPython(map_existing_choices, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="event",
            name="category",
            field=models.CharField(
                choices=[
                    ("movies", "Movies"),
                    ("waterparks", "Water parks"),
                    ("attractions", "Attractions"),
                    ("live", "Live events"),
                    ("other", "Other"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="ticketlisting",
            name="section",
            field=models.CharField(
                choices=[
                    ("standard", "Standard"),
                    ("premium", "Premium"),
                    ("vip", "VIP"),
                    ("family", "Family"),
                    ("day_pass", "Day pass"),
                ],
                max_length=20,
            ),
        ),
    ]
