from django.contrib import admin
from .models import *



@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email', 'table_number', 'date', 'time', 'num_guests']
    list_filter = ['table_number', 'date', 'time']
    search_fields = ['name', 'phone_number', 'email']


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'capacity', 'is_booked']
    list_filter = ['is_booked']

@admin.register(Contact)
class Contact1(admin.ModelAdmin):
    list_display = ['name', 'Email', 'comments',"phone"]



