

from django.shortcuts import render, HttpResponse
from django.utils.http import urlencode


# Create your views here.
def index(request):
    return render(request,'index.html')


def registration(request):
    return render(request, 'registration.html')


def free_menus(request):
    return render(request, 'free_menus.html')


def card(request):
    return render(request, 'card2.html')
