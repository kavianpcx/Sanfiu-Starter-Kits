from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SellerProfile, TicketListing

class SellerSignupForm(UserCreationForm):
    email=forms.EmailField(label="Email address")
    display_name=forms.CharField(max_length=120,label="Shop name")
    class Meta: model=User; fields=("username","email","password1","password2")
    def save(self,commit=True):
        user=super().save(commit=False); user.email=self.cleaned_data["email"]
        if commit: user.save(); SellerProfile.objects.create(user=user,display_name=self.cleaned_data["display_name"])
        return user

class TicketListingForm(forms.ModelForm):
    class Meta:
        model=TicketListing
        fields=("event","section","details","price","quantity_available")
        widgets={"details":forms.Textarea(attrs={"rows":3})}

class TicketPurchaseForm(forms.Form):
    buyer_name=forms.CharField(max_length=120,label="Full name")
    buyer_email=forms.EmailField(label="Email address")
    quantity=forms.IntegerField(min_value=1,max_value=8,initial=1,label="Tickets")
