from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from foodplan_site.functions import menu
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from foodplan_site.models import Order


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
    user = User.objects.get(username=request.user)
    MONTH_PRICE = 300
    foods_intolerances = ['Рыба и морепродукты', 'Мясо', 'Зерновые', 'Продукты пчеловодства', 'Орехи и бобовые', 'Молочные продукты']
    context = {
        'foods_intolerances': foods_intolerances,
        'month_price': MONTH_PRICE,
    }
    if request.GET:
        order_data = {
            'month_duration': int(request.GET['month_duration']),
            'breakfast': request.GET['select1'],
            'lunch': request.GET['select2'],
            'dinner': request.GET['select3'],
            'dessert': request.GET['select4'],
            'people_number': int(request.GET['select5']),
            'intolerances': [],
        }
        print(order_data)
        # for foods_intolerance in foods_intolerances:
        #     foods_intolerance = str(foods_intolerance)
        #     if foods_intolerance in request.GET:
        #         intolerance_id = request.GET[foods_intolerance]
        #         order_data['intolerances'].append(foods_intolerances.get(id=intolerance_id))

        order = Order.objects.create(
            user=user,
            breakfast=order_data['breakfast'],
            diner=order_data['dinner'],
            supper=order_data['lunch'],
            dessert=order_data['dessert'],
            person=order_data['people_number'],
            period=order_data['month_duration'],
            # total_sum=round(MONTH_PRICE * order_data['month_duration'], 2),
        )
        # order.intolerance.set(order_data['intolerances'])
        # description = f"""
        #             Подписка на {order.month_count} месяц(а)
        #             Аллергены: {[intolerance.name for intolerance in order_data['intolerances']]}
        #             """
        # return_url = f'http://{request.META["HTTP_HOST"]}/?' + urlencode({'order_id': order.id})

        # payment = create_payment(ACCOUNT_ID, U_KEY, description, return_url, order)
        # confirmation_url = payment.confirmation.confirmation_url

        # order.yookassa_id = payment.id
        # order.save()

        # return redirect(confirmation_url)
    return render(request, 'users/order.html')
