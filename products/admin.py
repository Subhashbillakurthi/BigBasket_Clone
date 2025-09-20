from django.contrib import admin
from .models import Category, Product, Pack,SubCategory, SubSubCategory

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Pack)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)