import random
from foodplan_site.models import Receipt, Product, ProductInReceipt, Order


def choosing(some_list):
    if some_list:
        return random.choice(some_list)
    return 'время голодать'


def menu(user_id):
    orders = Order.objects.filter(user_id=user_id).filter(paid=True)
    for order in orders:
        print('order>>', order)
        invalid_products_in_receipt = ProductInReceipt.objects.exclude(
            product__in=Product.objects.exclude(specific__in=order.allergic))
        wrong_products = []
        if order.classic:
            for i in Product.objects.exclude(classic=True).values_list('id', flat=True):
                if i not in wrong_products:
                    wrong_products.append(i)
        if order.lowcarb:
            for i in Product.objects.exclude(lowcarb=True).values_list('id', flat=True):
                if i not in wrong_products:
                    wrong_products.append(i)
        if order.vegan:
            for i in Product.objects.exclude(vegan=True).values_list('id', flat=True):
                if i not in wrong_products:
                    wrong_products.append(i)
        if order.keto:
            for i in Product.objects.exclude(keto=True).values_list('id', flat=True):
                if i not in wrong_products:
                    wrong_products.append(i)
        wrong_rec = ProductInReceipt.objects.filter(product_id__in=wrong_products)
        receipts = [k for k in Receipt.objects.all() if
                    k not in [i.receipt for i in invalid_products_in_receipt] and k not in [i.receipt for i in
                                                                                            wrong_rec]]
        order.sut = range(1, order.period * 30 + 1)
        order.days = []
        for day in range(0, order.period * 30):
            order.days.append({})
            order.days[day]['num'] = day + 1
            if order.breakfast:
                receipts_br = [k for k in receipts if k.breakfast]
                order.days[day]['breakfast'] = choosing(receipts_br)
            if order.diner:
                receipts_din = [k for k in receipts if k.diner]
                order.days[day]['diner'] = choosing(receipts_din)
            if order.supper:
                receipts_sup = [k for k in receipts if k.supper]
                order.days[day]['supper'] = choosing(receipts_sup)
            if order.dessert:
                receipts_des = [k for k in receipts if k.dessert]
                order.days[day]['dessert'] = choosing(receipts_des)
    return orders
