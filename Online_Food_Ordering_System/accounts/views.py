from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import NewUSerForm
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from django.shortcuts import render
from main.models import Item
from main.models import CartItems
from main.decorators import *
# from django.db.models import Sum
import razorpay


def homepage(request):
    return render(request,'order_details.html')



def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:login')
    else:
        form = NewUSerForm()
    return render(request, 'accounts/signup.html', { 'form': form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('main:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', { 'form': form })

def logout_view(request):
    if request.method == 'POST':
            logout(request)
            return redirect('/')


def staff_signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:stafflogin')
    else:
        form = NewUSerForm()
    return render(request, 'accounts/staff_signup.html', { 'form': form })

def staff_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('accounts:stafforder')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/staff_login.html', { 'form': form })

def staff_logout_view(request):
    if request.method == 'POST':
            logout(request)
            return redirect('/')

def staff_order_details(request):

    items = CartItems.objects.filter(user=request.user, ordered=True,status="Active").order_by('-ordered_date')
    cart_items = CartItems.objects.filter(user=request.user, ordered=True,status="Delivered").order_by('-ordered_date')
    # number = items.aggregate(Sum('quantity'))


    context = {
        'items':items,
        'cart_items':cart_items,
        # 'number':number,

    }
    return render(request, 'accounts/items.html', context)