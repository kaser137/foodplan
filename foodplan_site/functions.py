import random

from foodplan_site.models import Receipt, Product, ProductInReceipt, Order, Price


def choosing(some_list):
    if some_list:
        return random.choice(some_list)
    return 'время голодать'


def menu(user_id):
    orders = Order.objects.filter(user_id=user_id).filter(paid=True)
    for order in orders:
        invalid_products_in_receipt = ProductInReceipt.objects.exclude(
            product__in=Product.objects.exclude(specific__in=order.allergic))
        wrong_products = []
        if order.classic:
            wrong_products = [i for i in Product.objects.exclude(classic=True).values_list('id', flat=True)]
        if order.lowcarb:
            if not wrong_products and not order.classic:
                wrong_products = [i for i in Product.objects.exclude(lowcarb=True).values_list('id', flat=True)]
            else:
                w = []
                for i in Product.objects.exclude(lowcarb=True).values_list('id', flat=True):
                    for k in wrong_products:
                        if k == i:
                            w.append(k)
                    wrong_products = w
        if order.vegan:
            if not wrong_products and not order.classic and not order.lowcarb:
                wrong_products = [i for i in Product.objects.exclude(vegan=True).values_list('id', flat=True)]
            else:
                w = []
                for i in Product.objects.exclude(vegan=True).values_list('id', flat=True):
                    for k in wrong_products:
                        if k == i:
                            w.append(k)
                    wrong_products = w
        if order.keto:
            if not wrong_products and not order.classic and not order.lowcarb and not order.vegan:
                wrong_products = [i for i in Product.objects.exclude(keto=True).values_list('id', flat=True)]
            else:
                w = []
                for i in Product.objects.exclude(keto=True).values_list('id', flat=True):
                    for k in wrong_products:
                        if k == i:
                            w.append(k)
                    wrong_products = w
        wrong_products_in_receipt = ProductInReceipt.objects.filter(product_id__in=wrong_products)
        receipts = [k for k in Receipt.objects.all() if
                    k not in [i.receipt for i in invalid_products_in_receipt] and k not in [i.receipt for i in
                                                                                            wrong_products_in_receipt]]
        # order.sut = range(1, order.period * 30 + 1)
        order.days = []
        for day in range(0, order.period * 30):
            order.days.append({})
            order.days[day]['num'] = day + 1
            if order.breakfast:
                receipts_br = [k for k in receipts if k.breakfast]
                order.days[day]['breakfast'] = choosing(receipts_br)
            if order.dinner:
                receipts_din = [k for k in receipts if k.dinner]
                order.days[day]['dinner'] = choosing(receipts_din)
            if order.supper:
                receipts_sup = [k for k in receipts if k.supper]
                order.days[day]['supper'] = choosing(receipts_sup)
            if order.dessert:
                receipts_des = [k for k in receipts if k.dessert]
                order.days[day]['dessert'] = choosing(receipts_des)
    return orders


def cost(dictionary):
    price = Price.objects.last()
    attrs_price = price.__dict__
    del attrs_price['id'], attrs_price['_state']
    amount = 0
    for attr in attrs_price:
        attr_order = dictionary.get(attr, None)
        if attr_order:
            amount += dictionary['period'] * 30 * attrs_price[attr]
    return amount*dictionary['person']*(1-dictionary['discount']/100)
