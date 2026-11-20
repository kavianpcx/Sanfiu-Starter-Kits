from .models import Category


def marketplace_nav(request):
    categories = Category.objects.filter(
        products__is_active=True,
        products__seller__review_status="approved",
    ).distinct()
    cart = request.session.get("cart", {})
    count = 0
    for quantity in cart.values():
        try:
            count += max(0, int(quantity))
        except (TypeError, ValueError):
            continue
    return {"nav_categories": categories, "cart_count": count}
