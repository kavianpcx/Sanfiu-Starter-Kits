from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator

from .models import Product, Seller


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120, label="Full name")
    email = forms.EmailField(label="Email address")
    phone = forms.CharField(max_length=32, label="Phone number")
    city = forms.CharField(max_length=80)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    postal_code = forms.CharField(max_length=20, required=False)
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "category", "name", "slug", "summary", "description", "price",
            "compare_at_price", "image_url", "stock",
        )


class SellerRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, validators=[UnicodeUsernameValidator()])
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    store_name = forms.CharField(max_length=100, label="Store name")
    store_slug = forms.SlugField(max_length=120, label="Store URL name")
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError("That username is already in use.")
        return username

    def clean_store_slug(self):
        slug = self.cleaned_data["store_slug"]
        if Seller.objects.filter(slug=slug).exists():
            raise ValidationError("That store URL is already in use.")
        return slug

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password1")
        confirmation = cleaned.get("password2")
        if password and confirmation and password != confirmation:
            self.add_error("password2", "The passwords do not match.")
        if password and not self.has_error("password1"):
            try:
                user = get_user_model()(
                    username=cleaned.get("username", ""),
                    email=cleaned.get("email", ""),
                )
                validate_password(password, user=user)
            except ValidationError as error:
                self.add_error("password1", error)
        return cleaned

    def save(self):
        User = get_user_model()
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
        )
        seller = Seller.objects.create(
            user=user,
            store_name=self.cleaned_data["store_name"],
            slug=self.cleaned_data["store_slug"],
            description=self.cleaned_data["description"],
        )
        return user, seller
