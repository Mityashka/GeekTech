from django.contrib import admin
from .models import Product, Category, ProductImage, Feedback, Promotion, Delivery, Contact, Order, OrderItem



class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('product_name',)
    filter_horizontal = ('images',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price')
    readonly_fields = ('created_at', 'total_price', 'display_products')
    fields = ('user', 'created_at', 'total_price', 'display_products')

    def display_products(self, obj):
        return ", ".join([f"{item.product.product_name} - {item.quantity} шт." for item in obj.items.all()])
    display_products.short_description = "Продукты в заказе"


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Feedback)
admin.site.register(Promotion)
admin.site.register(Delivery)
admin.site.register(Contact)
admin.site.register(Order, OrderAdmin)
