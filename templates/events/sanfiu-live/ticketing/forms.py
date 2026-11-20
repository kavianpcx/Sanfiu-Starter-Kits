from django import forms


class BookingForm(forms.Form):
    attendee_name = forms.CharField(max_length=120, label="Your name")
    email = forms.EmailField(label="Email address")
    phone = forms.CharField(max_length=32, label="Phone number")
    quantity = forms.IntegerField(min_value=1, max_value=8, initial=1, label="Tickets")
