from django import forms
from .models import *

from django.core import validators
from django.core.validators import RegexValidator
from django.forms import DecimalField
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title","description","price","instructions","image","slug","created_by"]

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ["user","item","rslug","review","posted_on"]

# class CartItemsForm(forms.ModelForm):
#     class Meta:
#         model = CartItems
#         fields = ["user","item","ordered","quantity","ordered_data","status","delivery_date"]

class Customer_Form(forms.ModelForm):
    customer_name=forms.CharField(initial='First Name', required=True)
    Email=forms.EmailField(initial='Enter your email', required=True,validators=[validators.EmailValidator(message="Invalid Email")])
    # cusphone_number=forms.CharField(widget=forms.NumberInput())
    cusphone_number = forms.CharField(max_length=13, validators=[RegexValidator(
                      '^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$',
                      message="Enter a Valid Indian Phone Number")])
    class Meta:
        model = Customer
        fields = ["customer_name","Email","cusphone_number"]



class ContactForm(forms.ModelForm):
    customer_name = forms.CharField(initial='First Name', required=True)
    phone = forms.CharField(max_length=13, validators=[RegexValidator(
                      '^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$',
                      message="Enter a Valid Indian Phone Number")])
    email = forms.EmailField(initial='Enter your email', required=True,
                             validators=[validators.EmailValidator(message="Invalid Email")])
    Comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta:
        model=Contact
        fields=["customer_name","phone","email","Comment"]



class FeedbackForm(forms.ModelForm):
    customer_name = forms.CharField(initial='First Name', required=True)
    email = forms.EmailField(initial='Enter your email', required=True,
                             validators=[validators.EmailValidator(message="Invalid Email")])
    Details = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta:
            model=Feedback
            fields=["customer_name","Email","Details","Review"]

#
#
#
class staff_signupform(UserCreationForm):
    # image = forms.ImageField()
    password2 = forms.CharField(label="Confirmed_Password",widget=forms.PasswordInput)
    address = forms.CharField(max_length=1000,help_text="Address")
    contact = forms.CharField(max_length=13,help_text="Cotactno")
    sex = [('M', "Male"), ('F', "Female")]
    gender = forms.ChoiceField(choices=sex)

    class Meta:
        model = User
        fields = ['username','email','address','contact','gender']
        labels = {'email':'Email'}
class staff_editform(UserChangeForm):
    password = None
    address = forms.CharField(max_length=1000, help_text="Address")
    contact = forms.CharField(max_length=13, help_text="Cotactno")
    sex = [('M', "Male"), ('F', "Female")]
    gender = forms.ChoiceField(choices=sex)
    class Meta:
        model = User
        fields = ['username','email','address','contact','gender']
        labels = {'email':'Email'}











