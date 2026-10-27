"""
Django Admin configuration for the Lumera Cosmetics store.

The admin panel lets you:
- Add, edit, and delete products
- Manage categories
- View and update orders
- View registered customers (via the built-in User model)
"""

from django.contrib import admin
from .models import Category, Product, Order, OrderItem


# ── Category Admin ──────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# ── Product Admin ───────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating', 'stock', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_featured', 'rating')
    prepopulated_fields = {'slug': ('name',)}


# ── OrderItem Admin (inline inside Order) ───────────────────
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'quantity', 'subtotal')


# ── Order Admin ─────────────────────────────────────────────
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'city', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'city')
    list_editable = ('status',)
    inlines = [OrderItemInline]