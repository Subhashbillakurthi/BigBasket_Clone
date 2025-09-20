# vendor/forms.py
from django import forms
from products.models import Product, Category

# vendor/forms.py (or products/forms.py)
from django import forms
from products.models import Product, Category
from vendor.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "brand",
            "description",
            "weight",
            "weight_250g",
            "price_250g",
            "mrp",
            "price",
            "discount_percent",
            "price_per_g",
            "image",
            "image1",
            "image2",
            "image3",
            "quantity"
        ]
        # notice: 'vendor' is NOT included here


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields ='__all__'