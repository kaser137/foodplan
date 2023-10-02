import random

import foodplan_site
from foodplan_site.models import Receipt, Product, ProductInReceipt, Order, Price, Promo


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
        if attr_order != '0':
            amount += dictionary['period'] * 30 * attrs_price[attr]
    return amount * dictionary['person'] * (1 - dictionary['discount'] / 100)


def make_order_dict(request):
    order_data = {
        'period': int(request.GET['month_duration']),
        'breakfast': request.GET['select1'],
        'dinner': request.GET['select2'],
        'supper': request.GET['select3'],
        'dessert': request.GET['select4'],
        'person': int(request.GET['select5']) + 1,
        'classic': False,
        'lowcarb': False,
        'vegan': False,
        'keto': False,
        'allergic': [],
        'promo': request.GET['promo'],
    }
    if request.GET['foodtype'] == 'classic':
        order_data['classic'] = True
    if request.GET['foodtype'] == 'low':
        order_data['lowcarb'] = True
    if request.GET['foodtype'] == 'veg':
        order_data['vegan'] = True
    if request.GET['foodtype'] == 'keto':
        order_data['keto'] = True
    for num_allergen in range(1, 7):
        allergen = f'allergy{num_allergen}'
        if allergen in request.GET:
            order_data[allergen] = True
            order_data['allergic'].append(num_allergen)
    try:
        promo = Promo.objects.get(promokod=order_data['promo'])
        order_data['discount'] = promo.discount
    except foodplan_site.models.Promo.DoesNotExist:
        order_data['discount'] = 0
    return order_data
