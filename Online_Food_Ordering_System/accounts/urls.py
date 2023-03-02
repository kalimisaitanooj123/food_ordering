from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('staffsignup/', views.staff_signup_view, name="staffsignup"),
    path('stafflogin/', views.staff_login_view, name="stafflogin"),
    path('stafflogout/', views.staff_logout_view, name="stafflogout"),
    path('stafforder/', views.staff_order_details, name="stafforder"),
]
