import random

from foodplan_site.models import Receipt, Product, ProductInReceipt, Order


def choosing(l):
    if l:
        return random.choice(l)
    return 'время голодать'


def menu(user_id):
    orders = Order.objects.filter(user_id=user_id)
    for order in orders:
        print('order>>', order)
        invalid_products_in_receipt = ProductInReceipt.objects.exclude(
            product__in=Product.objects.exclude(specific__in=order.allergic))
        receipts = [k for k in Receipt.objects.all() if k not in [i.receipt for i in invalid_products_in_receipt]]
        print('rec>>>>', receipts)
        order.sut = range(1, order.period * 30 + 1)
        order.days = []
        print('6666', order.days)
        for day in range(0, order.period * 30):
            order.days.append({})
            order.days[day]['num'] = day + 1

            print('8888', order.days)
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
