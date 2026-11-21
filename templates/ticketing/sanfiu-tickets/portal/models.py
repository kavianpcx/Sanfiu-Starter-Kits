import uuid
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

class Event(models.Model):
    CATEGORY_CHOICES=[("music","Music"),("sports","Sports"),("arts","Arts & theatre"),("comedy","Comedy"),("other","Other") ]
    title=models.CharField(max_length=150)
    slug=models.SlugField(max_length=170,unique=True)
    category=models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    summary=models.CharField(max_length=220)
    description=models.TextField(blank=True)
    venue=models.CharField(max_length=140)
    city=models.CharField(max_length=80)
    starts_at=models.DateTimeField()
    image_url=models.URLField(max_length=500,blank=True)
    is_featured=models.BooleanField(default=False)
    is_published=models.BooleanField(default=True)
    class Meta: ordering=["starts_at"]
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse("event_detail",kwargs={"slug":self.slug})

class SellerProfile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="ticket_seller_profile")
    display_name=models.CharField(max_length=120)
    is_approved=models.BooleanField(default=False)
    joined_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.display_name

class TicketListing(models.Model):
    SECTION_CHOICES=[("general","General admission"),("floor","Floor"),("lower","Lower level"),("upper","Upper level"),("vip","VIP") ]
    event=models.ForeignKey(Event,on_delete=models.PROTECT,related_name="ticket_listings")
    seller=models.ForeignKey(SellerProfile,on_delete=models.PROTECT,related_name="listings")
    section=models.CharField(max_length=20,choices=SECTION_CHOICES)
    details=models.CharField(max_length=200,blank=True)
    price=models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(0)])
    quantity_available=models.PositiveSmallIntegerField(default=1)
    is_published=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["price","created_at"]
    def __str__(self): return f"{self.event.title} · {self.get_section_display()}"
    @property
    def sold_out(self): return self.quantity_available<1

class TicketOrder(models.Model):
    STATUS_CHOICES=[("reserved","Reserved"),("cancelled","Cancelled")]
    public_id=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    buyer_name=models.CharField(max_length=120)
    buyer_email=models.EmailField()
    total=models.DecimalField(max_digits=9,decimal_places=2,default=0)
    status=models.CharField(max_length=16,choices=STATUS_CHOICES,default="reserved")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-created_at"]
    def __str__(self): return f"Ticket order {self.public_id}"

class TicketOrderItem(models.Model):
    order=models.ForeignKey(TicketOrder,on_delete=models.CASCADE,related_name="items")
    listing=models.ForeignKey(TicketListing,on_delete=models.PROTECT,related_name="order_items")
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=8,decimal_places=2)
    def __str__(self): return f"{self.listing} × {self.quantity}"
