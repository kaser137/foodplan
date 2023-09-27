from django.shortcuts import render


def login(request):
    return render(request, 'users/auth.html')


def registration(request):
    return render(request, 'users/registration.html')
