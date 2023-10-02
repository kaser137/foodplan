from django.contrib import admin
from django.utils.html import format_html

from foodplan_site.models import Product, Receipt, ProductInReceipt, Order, Price, Promo


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


class ProductInReceiptInline(admin.TabularInline):
    model = ProductInReceipt

    readonly_fields = [
        'calories',
        'allergen',
    ]
    extra = 0


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    readonly_fields = [
        'preview',
        'calories',
    ]

    @staticmethod
    def preview(obj):
        return format_html('<img src="{}" style="max-height: {}px;" />',
                           obj.image.url,
                           200,
                           )
    inlines = [
        ProductInReceiptInline,
    ]
    extra = 0


@admin.register(ProductInReceipt)
class ProductInReceiptAdmin(admin.ModelAdmin):
    readonly_fields = [
        'calories',
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = [
        'cost',
    ]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    pass
