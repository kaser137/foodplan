from django.shortcuts import render, redirect

from foodplan_site.models import Receipt


# Create your views here.
def index(request):
    return render(request, 'index.html')


def registration(request):
    return render(request, 'registration.html')


def free_menus(request):
    receipt_chart = list(Receipt.objects.all().values_list('id', flat=True)[:3])
    for i in range(3):
        try:
            receipt_chart[i]
        except IndexError:
            receipt_chart.append(None)
    context = {
        'receipt_chart': receipt_chart
    }
    return render(request, 'free_menus.html', context=context)


def card(request):
    receipt_id = request.GET.get('receipt_id', None)
    print(receipt_id)
    print(type(receipt_id))
    if receipt_id and receipt_id != 'None':
        receipt = Receipt.objects.get(id=receipt_id)
        products = receipt.products.all()
        context = {
            'receipt': receipt,
            'products': products,
        }
        return render(request, 'card2.html', context=context)
    else:
        return redirect('index')


def lk(request):
    return render(request, 'lk.html')
