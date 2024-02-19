from django.db import models
from django.urls import reverse

# Create your models here.

class Color(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.user.username


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    old_price = models.FloatField(null=True, blank=True, default=None)
    description = models.TextField()
    image = models.ImageField(upload_to='products')
    colors = models.ManyToManyField('Color')
    sizes = models.ManyToManyField('Size')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})
    
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name