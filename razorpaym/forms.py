from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)

    class Meta:
        model = Address
        fields = ['customer_name', 'customer_email', 'customer_phone', 
                  'address_line', 'city', 'state', 'pincode', 'is_default']