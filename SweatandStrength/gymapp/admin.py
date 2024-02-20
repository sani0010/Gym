from django.contrib import admin
from .models import Trainer, Product, ProductImage

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ('title', 'product_image', 'description')

admin.site.register(Trainer)
admin.site.register(Product, ProductAdmin)
