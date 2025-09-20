from django.db import models
from vendor.models import Vendor
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Main Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    main_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return f"{self.main_category.name} > {self.name}"


class SubSubCategory(models.Model):
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="subsubcategories"
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Sub-Sub Categories"

    def __str__(self):
        return f"{self.sub_category.main_category.name} > {self.sub_category.name} > {self.name}"



class Product(models.Model):
    category = models.ForeignKey(SubSubCategory, on_delete=models.CASCADE, related_name='products',null=True,blank=True)
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',null=True,blank=True)
    name = models.CharField(max_length=100)
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='products'
    )

    brand = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0,blank=True, null=True)

    # Product default pack
    weight = models.CharField(max_length=50, null=True, blank=True)   # e.g. "500g"
    weight_250g = models.CharField(max_length=50, null=True, blank=True)
    price_250g = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    mrp = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    price_per_g = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # Images
    image = models.CharField(max_length=500, blank=True, null=True)
    image1 = models.CharField(max_length=500, blank=True, null=True)
    image2 = models.CharField(max_length=500, blank=True, null=True)
    image3 = models.CharField(max_length=500, blank=True, null=True)

    @property
    def is_out_of_stock(self):
        return self.quantity == 0
    
    def __str__(self):
        return self.name


class Pack(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='packs'
    )
    
    weight = models.CharField(max_length=50)
    mrp = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    price_per_g = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.weight} ({self.product.name})"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
