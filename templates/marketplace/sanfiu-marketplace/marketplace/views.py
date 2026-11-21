from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import cart_details
from .forms import CheckoutForm, ProductForm, SellerRegistrationForm
from .models import Category, Order, OrderItem, Product, Seller


def storefront(request):
    products = Product.objects.filter(
        is_active=True, seller__review_status=Seller.ReviewStatus.APPROVED
    ).select_related("category", "seller")
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(summary__icontains=query)
            | Q(description__icontains=query)
            | Q(seller__store_name__icontains=query)
        )
    if category_slug:
        products = products.filter(category__slug=category_slug)
    categories = Category.objects.filter(
        products__is_active=True,
        products__seller__review_status=Seller.ReviewStatus.APPROVED,
    ).distinct()
    return render(
        request,
        "marketplace/storefront.html",
        {"products": products, "categories": categories, "query": query, "selected_category": category_slug},
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("seller", "category"),
        slug=slug,
        is_active=True,
        seller__review_status=Seller.ReviewStatus.APPROVED,
    )
    return render(request, "marketplace/product_detail.html", {"product": product})


def store_page(request, slug):
    seller = get_object_or_404(Seller, slug=slug, review_status=Seller.ReviewStatus.APPROVED)
    products = seller.products.filter(is_active=True).select_related("category")
    return render(request, "marketplace/store_page.html", {"seller": seller, "products": products})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(
        Product,
        pk=product_id,
        is_active=True,
        seller__review_status=Seller.ReviewStatus.APPROVED,
    )
    if product.stock < 1:
        messages.error(request, "This item is currently out of stock.")
        return redirect(product.get_absolute_url())
    try:
        quantity = max(1, int(request.POST.get("quantity", "1")))
    except (TypeError, ValueError):
        quantity = 1
    cart_data = request.session.get("cart", {})
    key = str(product.pk)
    try:
        current = int(cart_data.get(key, 0))
    except (TypeError, ValueError):
        current = 0
    cart_data[key] = min(current + quantity, product.stock)
    request.session["cart"] = cart_data
    messages.success(request, f"{product.name} added to your bag.")
    return redirect("cart")


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_data = request.session.get("cart", {})
    key = str(product.pk)
    try:
        quantity = max(0, int(request.POST.get("quantity", "0")))
    except (TypeError, ValueError):
        quantity = 0
    if quantity == 0 or not product.is_active or product.stock == 0 or product.seller.review_status != Seller.ReviewStatus.APPROVED:
        cart_data.pop(key, None)
    else:
        cart_data[key] = min(quantity, product.stock)
    request.session["cart"] = cart_data
    return redirect("cart")


def cart(request):
    items, subtotal = cart_details(request)
    return render(request, "marketplace/cart.html", {"items": items, "subtotal": subtotal})


def checkout(request):
    items, subtotal = cart_details(request)
    if not items:
        messages.info(request, "Add an item to your bag before checkout.")
        return redirect("storefront")
    form = CheckoutForm(data=request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        requested = {}
        for product_id, quantity in request.session.get("cart", {}).items():
            try:
                requested[int(product_id)] = int(quantity)
            except (TypeError, ValueError):
                continue
        with transaction.atomic():
            products = {
                product.pk: product
                for product in Product.objects.select_for_update().filter(
                    pk__in=requested,
                    is_active=True,
                    seller__review_status=Seller.ReviewStatus.APPROVED,
                )
            }
            if any(
                quantity < 1 or product_id not in products or products[product_id].stock < quantity
                for product_id, quantity in requested.items()
            ):
                messages.error(request, "Stock changed while you were shopping. Review your bag and try again.")
                return redirect("cart")
            total = sum(
                (products[product_id].price * quantity for product_id, quantity in requested.items()),
                Decimal("0.00"),
            )
            order = Order.objects.create(total=total, **form.cleaned_data)
            for product_id, quantity in requested.items():
                product = products[product_id]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    unit_price=product.price,
                    quantity=quantity,
                )
                product.stock -= quantity
                product.save(update_fields=["stock"])
        request.session["cart"] = {}
        return redirect("order_success", public_id=order.public_id)
    return render(request, "marketplace/checkout.html", {"form": form, "items": items, "subtotal": subtotal})


def order_success(request, public_id):
    order = get_object_or_404(Order, public_id=public_id)
    return render(request, "marketplace/order_success.html", {"order": order})


def seller_apply(request):
    form = SellerRegistrationForm(data=request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        user, seller = form.save()
        login(request, user)
        messages.success(request, "Your seller application is waiting for review.")
        return redirect("seller_dashboard")
    return render(request, "marketplace/seller_apply.html", {"form": form})


def seller_for_request(request):
    if not request.user.is_authenticated:
        return None
    try:
        return request.user.seller_profile
    except Seller.DoesNotExist:
        return None


@login_required(login_url="seller_login")
def seller_dashboard(request):
    seller = seller_for_request(request)
    if seller is None:
        return redirect("seller_apply")
    if seller.review_status != Seller.ReviewStatus.APPROVED:
        return render(request, "marketplace/seller_pending.html", {"seller": seller})
    products = seller.products.all()
    order_items = OrderItem.objects.filter(product__seller=seller).select_related("order", "product")
    return render(
        request,
        "marketplace/seller_dashboard.html",
        {
            "seller": seller,
            "products": products,
            "order_items": order_items,
            "fulfillment_choices": OrderItem.FulfillmentStatus.choices,
        },
    )


@login_required(login_url="seller_login")
def seller_product_new(request):
    seller = seller_for_request(request)
    if seller is None or seller.review_status != Seller.ReviewStatus.APPROVED:
        return HttpResponseForbidden("An approved seller account is required.")
    form = ProductForm(data=request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.seller = seller
        product.is_active = False
        product.is_featured = False
        product.save()
        messages.success(request, "Listing submitted. A store admin must publish it before customers can see it.")
        return redirect("seller_dashboard")
    return render(request, "marketplace/seller_product_form.html", {"form": form, "heading": "Add a listing"})


@login_required(login_url="seller_login")
def seller_product_edit(request, product_id):
    seller = seller_for_request(request)
    if seller is None or seller.review_status != Seller.ReviewStatus.APPROVED:
        return HttpResponseForbidden("An approved seller account is required.")
    product = get_object_or_404(Product, pk=product_id, seller=seller)
    form = ProductForm(data=request.POST if request.method == "POST" else None, instance=product)
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.is_active = False
        product.save()
        messages.success(request, "Listing updated and sent back for admin review.")
        return redirect("seller_dashboard")
    return render(request, "marketplace/seller_product_form.html", {"form": form, "heading": "Edit listing"})


@login_required(login_url="seller_login")
@require_POST
def seller_update_fulfillment(request, item_id):
    seller = seller_for_request(request)
    if seller is None or seller.review_status != Seller.ReviewStatus.APPROVED:
        return HttpResponseForbidden("An approved seller account is required.")
    item = get_object_or_404(OrderItem, pk=item_id, product__seller=seller)
    allowed = {choice[0] for choice in OrderItem.FulfillmentStatus.choices}
    status = request.POST.get("status", "")
    if status in allowed:
        item.fulfillment_status = status
        item.save(update_fields=["fulfillment_status"])
        messages.success(request, "Fulfillment status updated.")
    return redirect("seller_dashboard")
