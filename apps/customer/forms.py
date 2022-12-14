from django import forms
from phonenumber_field.formfields import PhoneNumberField

from apps.users.models import User

# from .models import Customer
from apps.delivery.models import Job


class BasicUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar')


# class BasicCustomerForm(forms.ModelForm):
#     avatar = forms.ImageField()
#
#     class Meta:
#         model = Customer
#         fields = ('avatar',)


class JobCreateStep1Form(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('name', 'description', 'category', 'size', 'quantity',
                  'photo')


class JobCreateStep2Form(forms.ModelForm):
    pickup_address = forms.CharField(required=True)
    pickup_name = forms.CharField(required=True)
    pickup_phone = PhoneNumberField(required=True)

    class Meta:
        model = Job
        fields = ('pickup_address', 'pickup_lat', 'pickup_lng',
                  'pickup_name', 'pickup_phone')


class JobCreateStep3Form(forms.ModelForm):
    delivery_address = forms.CharField(required=True)
    delivery_name = forms.CharField(required=True)
    delivery_phone = PhoneNumberField(required=True)

    class Meta:
        model = Job
        fields = ('delivery_address', 'delivery_lat', 'delivery_lng',
                  'delivery_name', 'delivery_phone')
