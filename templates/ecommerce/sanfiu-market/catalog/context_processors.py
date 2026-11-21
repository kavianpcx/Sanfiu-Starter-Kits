from .models import Category


def cart_summary(request):
    cart = request.session.get("cart", {})
    count = 0
    for quantity in cart.values():
        try:
            count += max(0, int(quantity))
        except (TypeError, ValueError):
            continue
    nav_categories = Category.objects.filter(products__is_active=True).distinct()
    return {"cart_count": count, "nav_categories": nav_categories}
