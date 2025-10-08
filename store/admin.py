from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'products_list', 'total_items', 'total_amount')
    inlines = [OrderItemInline]

    # List of product names in the order
    def products_list(self, obj):
        return ", ".join([item.product.name for item in obj.items.all()])
    products_list.short_description = 'Products'

    # Total quantity of items
    def total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
    total_items.short_description = 'Items'

    # Total price of order
    def total_amount(self, obj):
        return sum(item.quantity * item.price for item in obj.items.all())
    total_amount.short_description = 'Total (₱)'

# Register models
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
