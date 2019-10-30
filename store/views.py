from django.shortcuts import render
from django.shortcuts import redirect
from .forms import UserForm
from .models import UserProfileInfo, Item,  Сheckout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal




def index(request):                   # Показ 10 товаров
    item = Item.objects.all()[:10]
    return render(request, 'index.html',{'item': item,})

@login_required
def cart(request):
    if 'items' not in request.session:
        return HttpResponse("В вашей корзине нет товаров!!!")
    if 'items' in request.session:
        items = Item.objects.filter(pk__in=request.session['items'])     # Корзина
        if not items:
            return redirect('no_cart')
        else:
            return render(request, 'cart.html',{'items': items})

@login_required
def no_cart(request):
    return render(request, 'no_cart.html',{})      # Отсутствие корзины

def item_detail(request, pk):
    product = Item.objects.get(pk=pk)                                     # Страница товара
    return render(request, 'product.html',{'product': product})

@login_required
def add_cart(request, pk):                  
    if 'items' not in request.session:
        request.session['items'] = []
    if pk not in request.session['items']:
        request.session['items'].append(pk)                                # Добавление товара в корзину 
        request.session.modified = True
        return redirect('index')
    else:
        cart_id = 'Товар уже присутствует в корзине!'
        return render(request, 'add_cart.html',{'cart_id': cart_id})


@login_required
def remove_item(request, pk):
    if pk in request.session['items']:
        request.session['items'].remove(pk)                                # Удаление товара из корзины
        request.session.modified = True
        return redirect('index')


@login_required
def checkout(request):
    items_id = request.session['items']                              # Оформление заказа
    items = Item.objects.filter(id__in=items_id)
    for item in items:
        checkout = Сheckout.objects.create(user=request.user,
                                        items_title=item.title,
                                        price=Decimal(item.price))
    del request.session['items']        
    return render(request, 'checkout.html',{})

@login_required
def list_checkout(request):
    items = Сheckout.objects.filter(user=request.user).order_by('-created_date')
    user = request.user
    if not items:
        return redirect('no_list_checkout')                             # Список покупок
    else:
        return render(request, 'list_checkout.html',{'items': items,'user': user})

@login_required
def no_list_checkout(request):
    return render(request, 'no_list_checkout.html',{})                     # Если человек ничего не купил


def find_item(request):               # Поиск нужного товара(Строг к регистру!!!)
    """
    :type request: object
    """
    q = request.GET.get("q")  # getting value from form
    try:
        product = Item.objects.get(title=q)  # check for user existence
    except:
        return render(request, 'search_error.html', {})  # redirect if there is no match
    else:
        return render(request, 'product.html', {'product': product})

@login_required
def user_logout(request):     # Выход пользователя из учетной записи
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):       # Регистрация пользователя
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request,user)
            registered = True
            return HttpResponseRedirect(reverse('index'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,'register.html',
                          {'user_form':user_form,
                           'registered':registered})


def user_login(request):                      # Вход пользователя в аккаунт
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})