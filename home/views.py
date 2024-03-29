from django.shortcuts import render
from .models import Campaign
from .forms import ContactForm
from shop.models import Category, Product

# Create your views here.

def home(request):
    campaigns = Campaign.objects.all()
    categories = Category.objects.all()
    return render(request, "index.html", {'campaigns': campaigns, 'categories': categories})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form_errors = form.errors
            return render(request, "contact.html", {'form_errors': form_errors, 'message': 'Your message not sent!', 'sent': False})
    elif request.method == 'GET':
        form = ContactForm()
        return render(request, "contact.html", {'form': form})
    return render(request, "contact.html", {'message': 'Your message has been sent!', 'sent': True})

def search_view(request):
    show_search = request.GET.get('search')
    down = Product.objects.filter(name__icontains=show_search)
    if down:
        return render(request, "search.html", {'products': down})
    else:
        return render(request, "search.html", {'message': 'No results found!'})