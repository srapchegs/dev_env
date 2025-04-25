from django.shortcuts import render
from product.models import Products, Categories

# Create your views here.

def detail(request, product_slug,category_slug):
    product = Products.objects.get(slug = product_slug,  category__category__slug=category_slug)
    context = {
        'title': "Детальная страница товара",
        "product": product
    }
    return render(request, 'product/detail.html', context=context)

def catalog(request, category_slug):
    products = Products.objects.filter(category__category__slug=category_slug)
    category = Categories.objects.get(slug=category_slug)
    context = {
        'category': category,
        "products": products
    }
    return render(request, 'product/catalog.html', context)
