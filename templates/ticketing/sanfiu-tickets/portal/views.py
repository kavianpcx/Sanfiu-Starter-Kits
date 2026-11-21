from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Min,Q
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import SellerSignupForm,TicketListingForm,TicketPurchaseForm
from .models import Event,SellerProfile,TicketListing,TicketOrder,TicketOrderItem

def event_list(request):
    events=Event.objects.filter(is_published=True,starts_at__gte=timezone.now()).annotate(lowest_price=Min("ticket_listings__price",filter=Q(ticket_listings__is_published=True,ticket_listings__seller__is_approved=True,ticket_listings__quantity_available__gt=0)))
    q=request.GET.get("q","").strip(); category=request.GET.get("category","").strip()
    if q: events=events.filter(Q(title__icontains=q)|Q(summary__icontains=q)|Q(venue__icontains=q)|Q(city__icontains=q))
    if category in dict(Event.CATEGORY_CHOICES): events=events.filter(category=category)
    return render(request,"portal/event_list.html",{"events":events,"featured_event":events.filter(is_featured=True).first(),"query":q,"selected_category":category})

def event_detail(request,slug):
    event=get_object_or_404(Event.objects.filter(is_published=True),slug=slug)
    listings=TicketListing.objects.filter(event=event,is_published=True,seller__is_approved=True,quantity_available__gt=0).select_related("seller")
    return render(request,"portal/event_detail.html",{"event":event,"listings":listings,"forms_by_listing":{item.pk:TicketPurchaseForm(prefix=str(item.pk)) for item in listings}})

@require_POST
def buy_ticket(request,listing_id):
    listing=get_object_or_404(TicketListing.objects.select_related("event","seller"),pk=listing_id,is_published=True,seller__is_approved=True)
    form=TicketPurchaseForm(request.POST,prefix=str(listing.pk))
    if not form.is_valid(): messages.error(request,"Check your name, email, and ticket quantity."); return redirect(listing.event.get_absolute_url())
    with transaction.atomic():
        listing=TicketListing.objects.select_for_update().get(pk=listing.pk)
        quantity=form.cleaned_data["quantity"]
        if listing.event.starts_at<=timezone.now() or listing.quantity_available<quantity:
            messages.error(request,"That ticket quantity is no longer available."); return redirect(listing.event.get_absolute_url())
        total=listing.price*quantity
        order=TicketOrder.objects.create(buyer_name=form.cleaned_data["buyer_name"],buyer_email=form.cleaned_data["buyer_email"],total=total)
        TicketOrderItem.objects.create(order=order,listing=listing,quantity=quantity,unit_price=listing.price)
        listing.quantity_available-=quantity; listing.save(update_fields=["quantity_available"])
    return redirect("order_confirmation",public_id=order.public_id)

def order_confirmation(request,public_id):
    order=get_object_or_404(TicketOrder.objects.prefetch_related("items__listing__event"),public_id=public_id)
    return render(request,"portal/order_confirmation.html",{"order":order})

def seller_signup(request):
    if request.user.is_authenticated: return redirect("seller_dashboard")
    form=SellerSignupForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        user=form.save(); login(request,user); messages.success(request,"Account created. Your seller profile needs admin approval before listings can go live."); return redirect("seller_dashboard")
    return render(request,"registration/signup.html",{"form":form})

@login_required
def seller_dashboard(request):
    seller=get_object_or_404(SellerProfile,user=request.user)
    listings=seller.listings.select_related("event")
    orders=TicketOrder.objects.filter(items__listing__seller=seller).distinct().prefetch_related("items__listing__event")
    return render(request,"portal/seller_dashboard.html",{"seller":seller,"listings":listings,"orders":orders})

@login_required
def create_listing(request):
    seller=get_object_or_404(SellerProfile,user=request.user)
    if not seller.is_approved: return render(request,"portal/seller_pending.html",{"seller":seller},status=403)
    form=TicketListingForm(request.POST or None)
    form.fields["event"].queryset=Event.objects.filter(is_published=True,starts_at__gt=timezone.now())
    if request.method=="POST" and form.is_valid():
        listing=form.save(commit=False); listing.seller=seller; listing.is_published=False; listing.save(); messages.success(request,"Listing submitted for review."); return redirect("seller_dashboard")
    return render(request,"portal/listing_form.html",{"form":form})
