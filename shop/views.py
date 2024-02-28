from django.shortcuts import render
from .models import Product, Category, Color, Size
from django.core.paginator import Paginator
# Create your views here.

def shop(request):
    products = Product.objects.all()
    page_input = request.GET.get('page', 1)
    paginator = Paginator(products, 3)
    page = paginator.page(page_input)
    products = page.object_list

    print(page)
    context = {
        'products': products,
        'paginator': paginator,
        'page': page,
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