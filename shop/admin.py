from django.contrib import admin
from .models import Product, Category, Color, Size, Review

# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Review)