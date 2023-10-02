from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth
from django.urls import reverse
from django.utils.http import urlencode
from foodplan_site import functions
import foodplan_site
from foodplan_site.functions import menu, make_order_dict
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from foodplan_site.models import Order, Promo
from yookassa import Configuration, Payment
from environs import Env
import uuid

order_data = {}
print('9999999999', order_data)
env = Env()
env.read_env()
ACCOUNT_ID = env('YOUKASSA_ACCOUNT_ID')
U_KEY = env('U_KEY')


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile'))

    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/auth.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    orders = menu(request.user.id)
    context = {
        'form': form,
        'orders': orders,
        'path': request.path
    }
    return render(request, 'users/lk.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def order(request):
    global order_data
    user = User.objects.get(username=request.user)
    if request.GET:
        order_id = request.GET.get('?!@', None)
        if order_id:
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()
            cost = '0000'
            return render(request, 'users/order.html', context={'cost': cost, 'dic': order_data})
        pay = request.GET.get('pay', None)
        if not pay:
            order_data = make_order_dict(request)
            cost = functions.cost(order_data)
            return render(request, 'users/order.html', context={'cost': cost, 'dic': order_data})
        else:
            if not order_data:
                order_data = make_order_dict(request)
            order = Order.objects.create(
                user=user,
                breakfast=order_data['breakfast'],
                dinner=order_data['dinner'],
                supper=order_data['supper'],
                dessert=order_data['dessert'],
                person=order_data['person'],
                period=order_data['period'],
                classic=order_data['classic'],
                lowcarb=order_data['lowcarb'],
                vegan=order_data['vegan'],
                keto=order_data['keto'],
                allergic=order_data['allergic'],
                discount=order_data['discount']
            )
            order.save()
            cost = functions.cost(order_data)
            order_data = {}
            redirect_url = 'http://127.0.0.1:8000/users/order/' + '?' + urlencode({'?!@': order.id})
            Configuration.account_id = ACCOUNT_ID
            Configuration.secret_key = U_KEY
            payment = Payment.create({
                "amount": {
                    "value": f"{cost}",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": redirect_url
                },
                "capture": True,
                "description": f"{order}",
                "metadata": {"order": order.id}
            }, uuid.uuid4())
            confirmation_url = payment.confirmation.confirmation_url
            return redirect(confirmation_url)
    else:
        context = {
            'cost': '0000',
            'dic': order_data
        }
    return render(request, 'users/order.html', context=context)
