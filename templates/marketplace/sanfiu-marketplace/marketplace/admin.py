from django.contrib import admin

from .models import Category, Order, OrderItem, Product, Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("store_name", "user", "review_status", "created_at")
    list_filter = ("review_status", "created_at")
    list_editable = ("review_status",)
    search_fields = ("store_name", "slug", "user__username", "user__email")
    prepopulated_fields = {"slug": ("store_name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "seller", "category", "price", "stock", "is_active")
    list_filter = ("seller", "category", "is_active")
    list_editable = ("price", "stock", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "seller__store_name", "summary")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ("product", "product_name", "unit_price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("public_id", "full_name", "email", "total", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("public_id", "full_name", "email", "phone")
    readonly_fields = ("public_id", "total", "created_at")
    inlines = (OrderItemInline,)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product_name", "product", "quantity", "fulfillment_status", "order")
    list_filter = ("fulfillment_status",)
    list_editable = ("fulfillment_status",)
    search_fields = ("product_name", "product__seller__store_name", "order__public_id")
