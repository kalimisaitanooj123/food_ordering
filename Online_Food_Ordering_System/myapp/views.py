from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render


from django.contrib.auth.decorators import login_required
from .decorators import *
from django.db.models import Sum



@login_required
def table_list(request):
    tables = Table.objects.filter(is_booked=False)
    return render(request, 'table_list.html', {'tables': tables})



def reservation(request):
    tables = Table.objects.filter(is_booked=False)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            table_number = form.cleaned_data['table_number']
            table = Table.objects.get(table_number=table_number)
            reservation = form.save(commit=False)
            reservation.table = table
            reservation.save()
            table.is_booked = True
            table.save()
            return redirect('myapp:reservation_success')
    else:
        form = ReservationForm()
    return render(request, 'reservation.html', {'form': form, 'tables': tables})



def reservation_success(request):
    return render(request, 'reservation_success.html')




def table_detail(request, pk):
    table = get_object_or_404(Table, pk=pk)
    return render(request, 'table_detail.html', {'table': table})



def Contactinfo(request):
    if request.method=='POST':
        data=Contactus(request.POST)
        if data.is_valid():
            n=data.cleaned_data["name"]
            e=data.cleaned_data["Email"]
            c=data.cleaned_data["comments"]
            p=data.cleaned_data["phone"]
            result=Contact(name=n,Email=e,comments=c,phone=p)

            result.save()
            messages.success(request, 'commented successfully!!!')
    else:
        data=Contactus()
    con=Contact.objects.all()
    return render(request,"contact.html",{"data1":data,"con1":con})

