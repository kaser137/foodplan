from django.shortcuts import render, HttpResponse
from django.utils.http import urlencode

from foodplan_site.models import Receipt


# Create your views here.
def index(request):
    return render(request, 'index.html')


def registration(request):
    return render(request, 'registration.html')


def free_menus(request):
    receipt_chart = Receipt.objects.all().values_list('id', flat=True)[:3]
    context ={
        'receipt_chart': receipt_chart
    }
    print(receipt_chart, '*****************************************')
    return render(request, 'free_menus.html', context=context)


def card(request):
    receipt_id = request.GET.get('receipt_id', None)
    if receipt_id:
        receipt = Receipt.objects.get(id=receipt_id)
        products = receipt.products.all()
        context = {
            'receipt': receipt,
            'products': products,
        }
    return render(request, 'card2.html', context=context)
