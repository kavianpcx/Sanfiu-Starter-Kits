from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

class Device(models.Model):
 CATEGORY_CHOICES=[("phone","Phones"),("computer","Computers"),("audio","Audio"),("accessory","Accessories")]
 title=models.CharField(max_length=140)
 slug=models.SlugField(max_length=160,unique=True)
 category=models.CharField(max_length=20,choices=CATEGORY_CHOICES)
 tagline=models.CharField(max_length=180)
 description=models.TextField()
 price=models.DecimalField(max_digits=9,decimal_places=2,validators=[MinValueValidator(0)])
 image_url=models.URLField(max_length=500,blank=True)
 finish=models.CharField(max_length=80,default="Midnight")
 display=models.CharField(max_length=80,blank=True)
 processor=models.CharField(max_length=100,blank=True)
 battery=models.CharField(max_length=100,blank=True)
 camera=models.CharField(max_length=100,blank=True)
 storage=models.CharField(max_length=100,blank=True)
 is_featured=models.BooleanField(default=False)
 is_published=models.BooleanField(default=False)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:ordering=["-is_featured","title"]
 def __str__(self):return self.title
 def get_absolute_url(self):return reverse("device_detail",kwargs={"slug":self.slug})

class Inquiry(models.Model):
 STATUS_CHOICES=[("new","New"),("contacted","Contacted"),("closed","Closed")]
 device=models.ForeignKey(Device,on_delete=models.PROTECT,related_name="inquiries")
 name=models.CharField(max_length=120)
 email=models.EmailField()
 phone=models.CharField(max_length=32,blank=True)
 message=models.TextField()
 status=models.CharField(max_length=16,choices=STATUS_CHOICES,default="new")
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:ordering=["-created_at"]
 def __str__(self):return f"{self.device.title} · {self.name}"
