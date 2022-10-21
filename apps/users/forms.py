from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Customer, Job


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=250)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email):
            raise ValidationError("This email address already exists.")
        return email


class BasicUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BasicCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('avatar',)


class JobCreateStep1Form(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('name', 'description', 'category', 'size', 'quantity',
                  'photo')


class JobCreateStep2Form(forms.ModelForm):
    pickup_address = forms.CharField(required=True)
    pickup_name = forms.CharField(required=True)
    pickup_phone = forms.CharField(required=True)

    class Meta:
        model = Job
        fields = ('pickup_address', 'pickup_lat', 'pickup_lng',
                  'pickup_name', 'pickup_phone')


class JobCreateStep3Form(forms.ModelForm):
    delivery_address = forms.CharField(required=True)
    delivery_name = forms.CharField(required=True)
    delivery_phone = forms.CharField(required=True)

    class Meta:
        model = Job
        fields = ('delivery_address', 'delivery_lat', 'delivery_lng',
                  'delivery_name', 'delivery_phone')
