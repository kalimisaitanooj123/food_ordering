from django.contrib import admin
from django.urls import path
from myapp import views

app_name = "myapp"

urlpatterns = [
    path('tables/', views.table_list, name='table_list'),
    path('tables/<int:pk>/', views.table_detail, name='table_detail'),
    path('reservation/', views.reservation, name='reservation'),
    path('reservation/success/', views.reservation_success, name='reservation_success'),
    path("contact", views.Contactinfo, name="contact"),

]