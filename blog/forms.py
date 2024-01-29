from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,User



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'mobile1', 'mobile2', 'landline', 'email', 'address', 'location']

class AddPropertyForm(forms.ModelForm):
    class Meta:
        model = AddProperty
        fields = ['profile_names', 'main_prop', 'prop_type', 'size_unit','prop_size', 'location', 'image', 'price_from','price_to', 'description', 'installment', 'persontype']

    def clean(self):
        cleaned_data = super().clean()
        price_from = cleaned_data.get('price_from')
        price_to = cleaned_data.get('price_to')

        if price_from is not None and price_to is not None and price_from > price_to:
            raise forms.ValidationError('Price from must be less than or equal to Price to')

class crmForm(forms.ModelForm):
    class Meta:
        model = crm
        fields = ['client_options','description']


class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm password (again) ",widget= forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email"]
        labels={"email":"Email"}