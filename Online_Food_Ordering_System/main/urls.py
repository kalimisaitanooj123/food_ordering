from django.contrib import admin
from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.Menu,name='menu1'),
    path('home/', views.menu_list_view, name="home"),
    path('maincourse/', views.Maincourse, name="main"),
    path('stratas/', views.Stratas, name="strata"),
    path('dishes/<int:id>', views.menuDetail, name='dishes'),
    path('item_list/', views.item_list, name='item_list'),
    path('item/new/', views.item_create_view, name='item-create'),
    path('item-update/<slug>/', views.update_item, name='item-update'),
    path('item-delete/<slug>/', views.item_delete, name='item-delete'),
    path('addtocart/<id>/', views.add_to_cart, name='addtocart'),
    path('cart/', views.get_cart_items, name='cart'),
    path('remove-from-cart/<int:pk>/', views.delete_cart_item, name='remove-from-cart'),
    path('ordered/', views.order_item, name='ordered'),
    path('order_details/', views.order_details, name='order_details'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('pending_orders/', views.pending_orders, name='pending_orders'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update_status/<int:pk>', views.update_status, name='update_status'),
    path('postReview', views.add_reviews, name='add_reviews'),
    path('about', views.aboutus, name='about'),
    path('pay', views.homepage, name='index'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),


]
