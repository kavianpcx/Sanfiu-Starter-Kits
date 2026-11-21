from django.db.models import Q
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from .forms import InquiryForm
from .models import Device

def device_list(request):
 devices=Device.objects.filter(is_published=True)
 q=request.GET.get("q","").strip(); category=request.GET.get("category","").strip()
 if q:devices=devices.filter(Q(title__icontains=q)|Q(tagline__icontains=q)|Q(description__icontains=q))
 if category in dict(Device.CATEGORY_CHOICES):devices=devices.filter(category=category)
 return render(request,"portal/device_list.html",{"devices":devices,"featured_device":devices.filter(is_featured=True).first(),"query":q,"selected_category":category})

def device_detail(request,slug):
 device=get_object_or_404(Device,is_published=True,slug=slug)
 form=InquiryForm(request.POST or None)
 if request.method=="POST" and form.is_valid():
  inquiry=form.save(commit=False);inquiry.device=device;inquiry.save();return redirect("inquiry_confirmation")
 return render(request,"portal/device_detail.html",{"device":device,"form":form})

def inquiry_confirmation(request):
 return render(request,"portal/inquiry_confirmation.html")
