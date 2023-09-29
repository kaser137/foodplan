from django.contrib import admin

from foodplan_site.models import Product, Receipt, ProductInReceipt, Order, Price


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
        'calories'
    ]
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
