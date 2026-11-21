from django.db import migrations,models
class Migration(migrations.Migration):
 initial=True
 dependencies=[]
 operations=[migrations.CreateModel(name="ClockCity",fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("name",models.CharField(max_length=100)),("region",models.CharField(blank=True,max_length=100)),("slug",models.SlugField(max_length=120,unique=True)),("timezone_name",models.CharField(help_text="Use an IANA timezone name, for example America/New_York.",max_length=80)),("is_featured",models.BooleanField(default=False)),("is_active",models.BooleanField(default=True)),("sort_order",models.PositiveSmallIntegerField(default=0))],options={"ordering":["sort_order","name"]})]
