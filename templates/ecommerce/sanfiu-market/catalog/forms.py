from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120, label="Full name")
    email = forms.EmailField(label="Email address")
    phone = forms.CharField(max_length=32, label="Phone number")
    city = forms.CharField(max_length=80)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    postal_code = forms.CharField(max_length=20, required=False)
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Optional"}),
    )
