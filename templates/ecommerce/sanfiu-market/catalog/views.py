from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import cart_details
from .forms import CheckoutForm
from .models import Category, Order, OrderItem, Product


def storefront(request):
    products = Product.objects.filter(is_active=True).select_related("category")
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(summary__icontains=query)
            | Q(description__icontains=query)
        )
    if category_slug:
        products = products.filter(category__slug=category_slug)
    categories = Category.objects.filter(products__is_active=True).distinct()
    return render(
        request,
        "catalog/storefront.html",
        {
            "products": products,
            "categories": categories,
            "query": query,
            "selected_category": category_slug,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(is_active=True).exclude(pk=product.pk)[:4]
    return render(
        request,
        "catalog/product_detail.html",
        {"product": product, "related_products": related_products},
    )


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    if product.stock < 1:
        messages.error(request, "This item is currently out of stock.")
        return redirect(product.get_absolute_url())
    try:
        requested_quantity = max(1, int(request.POST.get("quantity", "1")))
    except (TypeError, ValueError):
        requested_quantity = 1
    cart = request.session.get("cart", {})
    key = str(product.pk)
    try:
        current_quantity = int(cart.get(key, 0))
    except (TypeError, ValueError):
        current_quantity = 0
    cart[key] = min(current_quantity + requested_quantity, product.stock)
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your bag.")
    return redirect("cart")


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get("cart", {})
    key = str(product.pk)
    try:
        quantity = max(0, int(request.POST.get("quantity", "0")))
    except (TypeError, ValueError):
        quantity = 0
    if quantity == 0 or not product.is_active or product.stock == 0:
        cart.pop(key, None)
    else:
        cart[key] = min(quantity, product.stock)
    request.session["cart"] = cart
    return redirect("cart")


def cart(request):
    items, subtotal = cart_details(request)
    return render(request, "catalog/cart.html", {"items": items, "subtotal": subtotal})


def checkout(request):
    items, subtotal = cart_details(request)
    if not items:
        messages.info(request, "Add an item to your bag before checkout.")
        return redirect("storefront")

    form = CheckoutForm(data=request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        cart_data = request.session.get("cart", {})
        requested = {}
        for product_id, quantity in cart_data.items():
            try:
                quantity = int(quantity)
                product_id = int(product_id)
            except (TypeError, ValueError):
                continue
            if quantity > 0:
                requested[product_id] = quantity

        with transaction.atomic():
            products = {
                product.pk: product
                for product in Product.objects.select_for_update().filter(
                    pk__in=requested, is_active=True
                )
            }
            unavailable = [
                product_id
                for product_id, quantity in requested.items()
                if product_id not in products or products[product_id].stock < quantity
            ]
            if unavailable:
                messages.error(
                    request,
                    "Stock changed while you were shopping. Review your bag and try again.",
                )
                return redirect("cart")

            total = sum(
                (products[product_id].price * quantity
                 for product_id, quantity in requested.items()),
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
        messages.success(request, "Your order has been placed.")
        return redirect("order_success", public_id=order.public_id)

    return render(
        request,
        "catalog/checkout.html",
        {"form": form, "items": items, "subtotal": subtotal},
    )


def order_success(request, public_id):
    order = get_object_or_404(Order, public_id=public_id)
    return render(request, "catalog/order_success.html", {"order": order})
