from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, CartItems, Reviews
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, CartItems, Reviews
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from .models import Item
from .models import Item, CartItems, Reviews
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.db.models import Sum
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from django.shortcuts import render

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))


def homepage(request):
    currency = 'INR'
    amount = 100000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture=1))
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
    context = {
        'amount': 1000, 'api_key': settings.RAZORPAY_API_KEY, 'order_id': razorpay_order_id
    }


    return render(request, 'main/order_details.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 500  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    return render(request, 'main/paymentsuccess.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return render(request, 'main/paymentsuccess.html')
        # return HttpResponseBadRequest()

# authorize razorpay client with API Keys.



def aboutus(request):
    return render(request, 'main/about.html')


def Menu(request):
    return render(request,'main/menu.html')

def Stratas(request):
    menu_items = Item.objects.all()
    context = {'menu_items': menu_items}
    return render(request, 'main/stratas.html', context)

def menu_list_view(request):
    menu_items = Item.objects.all()
    context = {'menu_items': menu_items}
    return render(request, 'main/home.html', context)

def Maincourse(request):
    menu_items = Item.objects.all()
    context = {'menu_items': menu_items}
    return render(request, 'main/maincourse.html', context)


def menuDetail(request, id):
    item = Item.objects.get(id=id)
    return render(request, 'main/dishes.html', {'item':item})


@login_required
def add_reviews(request):
    if request.method == "POST":
        user = request.user
        rslug = request.POST.get("rslug")
        item = Item.objects.get(slug=rslug)
        review = request.POST.get("review")

        reviews = Reviews(user=user, item=item, review=review, rslug=rslug)
        reviews.save()
        messages.success(request, "Thank You for Reviewing this Item!!")
    return redirect(f"/dishes/{item.slug}")

def item_create_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('items')
    else:
        form = ItemForm()
    context = {'form': form}
    return render(request, 'main/item_form.html', context)


def update_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if request.user != item.created_by:
        return redirect('items:list')

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect('items:list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/item_form.html', {'form': form})




def item_delete(request, pk):
    item = Item.objects.get(pk=pk)
    if request.user == item.created_by:
        item.delete()
        return redirect('/item_list')
    return render(request, '403.html', {'message': 'You are not authorized to perform this action.'}, status=403)



@login_required
def add_to_cart(request, id):
    item = Item.objects.filter(id=id).first()
    if item:
        cart_item = CartItems.objects.create(
            item=item,
            user=request.user,
            ordered=False,
        )
        messages.info(request, "Added to Cart!!Continue Shopping!!")
        return redirect("main:cart")
    else:
        messages.warning(request, "Item not found")
        return redirect("main:home")


@login_required
def get_cart_items(request):
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    bill = cart_items.aggregate(Sum('item__price'))
    number = cart_items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    context = {
        'cart_items':cart_items,
        'total': total,
        'count': count,
    }
    return render(request, 'main/cart.html', context)

def delete_cart_item(request, pk):
    cart = CartItems.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.user == cart.user:
            cart.delete()
            return redirect('/cart')
        else:
            return redirect('/')
    else:
        return redirect('/login')


@login_required
def order_item(request):
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    ordered_date=timezone.now()
    cart_items.update(ordered=True,ordered_date=ordered_date)
    messages.info(request, "Item Ordered")
    return redirect("main:order_details")

@login_required
def order_details(request):
    items = CartItems.objects.filter(user=request.user, ordered=True).order_by('-ordered_date')
    cart_items = CartItems.objects.filter(user=request.user, ordered=True).order_by('-ordered_date')
    bill = items.aggregate(Sum('item__price'))
    number = items.aggregate(Sum('quantity'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    context = {
        'items':items,
        'cart_items':cart_items,
        'total': total,
        'count': count,

    }
    return render(request, 'main/order_details.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def admin_view(request):
    cart_items = CartItems.objects.filter(item__created_by=request.user, ordered=True).order_by('-ordered_date')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'main/admin_view.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def item_list(request):
    items = Item.objects.filter(created_by=request.user)
    context = {
        'items':items
    }
    return render(request, 'main/item_list.html', context)

@login_required
@admin_required
def update_status(request,pk):
    if request.method == 'POST':
        status = request.POST['status']
    cart_items = CartItems.objects.filter(item__created_by=request.user, ordered=True,pk=pk)
    delivery_date=timezone.now()
    # if status == 'Delivered':
    #     cart_items.update(status=status, delivery_date=delivery_date)
    return render(request, 'main/pending_orders.html')

@login_required(login_url='/accounts/login/')
@admin_required
def pending_orders(request):
    items = CartItems.objects.filter(item__created_by=request.user, ordered=True).order_by('-ordered_date')
    context = {
        'items':items,
    }
    return render(request, 'main/pending_orders.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def admin_dashboard(request):
    cart_items = CartItems.objects.filter(item__created_by=request.user, ordered=True)
    pending_total = CartItems.objects.filter(item__created_by=request.user, ordered=True).count()
    completed_total = CartItems.objects.filter(item__created_by=request.user, ordered=True).count()
    count1 = CartItems.objects.filter(item__created_by=request.user, ordered=True,item="3").count()
    count2 = CartItems.objects.filter(item__created_by=request.user, ordered=True,item="4").count()
    count3 = CartItems.objects.filter(item__created_by=request.user, ordered=True,item="5").count()
    total = CartItems.objects.filter(item__created_by=request.user, ordered=True).aggregate(Sum('item__price'))
    income = total.get("item__price__sum")
    context = {
        'pending_total' : pending_total,
        'completed_total' : completed_total,
        'income' : income,
        'count1' : count1,
        'count2' : count2,
        'count3' : count3,
    }
    return render(request, 'main/admin_dashboard.html', context)

