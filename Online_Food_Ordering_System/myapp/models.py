from django.db import models
from django.core.validators import MaxLengthValidator

class Table(models.Model):
    table_number = models.IntegerField()
    capacity = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.table_number}"

class Reservation(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    table_number = models.CharField(max_length=10)
    date = models.DateField()
    time = models.TimeField()
    num_guests = models.IntegerField()

    def __str__(self):
        return f"{self.name} - Table {self.table_number} - {self.date} {self.time}"


from django.shortcuts import render, get_object_or_404
from .models import Table

def table_detail(request, pk):
    table = get_object_or_404(Table, pk=pk)
    return render(request, 'table_detail.html', {'table': table})\



class Contact(models.Model):
    name = models.CharField(max_length=100)
    Email=models.EmailField(max_length=100)
    comments = models.CharField(max_length=100)
    phone=models.IntegerField(null=True)

    def __str__(self):
        return self.name


