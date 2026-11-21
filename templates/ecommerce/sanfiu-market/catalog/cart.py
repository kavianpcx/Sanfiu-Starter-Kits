from decimal import Decimal

from .models import Product


def cart_details(request):
    cart = request.session.get("cart", {})
    product_ids = []
    for product_id, quantity in cart.items():
        try:
            if int(quantity) > 0:
                product_ids.append(int(product_id))
        except (TypeError, ValueError):
            continue

    products = {
        str(product.pk): product
        for product in Product.objects.filter(pk__in=product_ids, is_active=True)
    }
    items = []
    subtotal = Decimal("0.00")
    for product_id, quantity in cart.items():
        product = products.get(str(product_id))
        if product is None:
            continue
        try:
            quantity = max(0, int(quantity))
        except (TypeError, ValueError):
            continue
        if quantity == 0:
            continue
        line_total = product.price * quantity
        items.append({"product": product, "quantity": quantity, "line_total": line_total})
        subtotal += line_total

    return items, subtotal
