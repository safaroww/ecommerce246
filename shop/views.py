from django.shortcuts import render
from .models import Product, Category, Color, Size

# Create your views here.

def shop(request):
    products = Product.objects.all()
    
    context = {
        'products': products,
    }
    return render(request, 'shop.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    sizes = product.sizes.all()
    colors = product.colors.all()
    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
    }
    return render(request, 'product-detail.html', context)