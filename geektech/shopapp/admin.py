from django.contrib import admin
from .models import Product, Category, ProductImage, Feedback, Promotion, Delivery, Contact



class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('product_name',)
    filter_horizontal = ('images',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Feedback)
admin.site.register(Promotion)
admin.site.register(Delivery)
admin.site.register(Contact)
