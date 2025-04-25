from django.shortcuts import render
from product.models import Products

# Create your views here.

def detail(request):
    context = {
        'title': "Детальная страница товара"
    }
    return render(request, 'product/detail.html', context)

def catalog(request):
    products = Products.objects.all()
    context = {
        'title': "Блоки",
        "products": products
    }
    return render(request, 'product/catalog.html', context)
