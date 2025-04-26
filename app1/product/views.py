from django.shortcuts import render
from product.models import Products, Categories, Subcategories

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
    subcategories = Subcategories.objects.filter(category=category)
    subcategory_slug = request.GET.get('subcategory')  # Получаем выбранную подкатегорию
    sort_order = request.GET.get('sort')
    if subcategory_slug:
        products = Products.objects.filter(category__slug=subcategory_slug, category__category=category)
    else:
        products = Products.objects.filter(category__category=category)
    if sort_order == 'asc':
        products = products.order_by('price')  # По возрастанию
    elif sort_order == 'desc':
        products = products.order_by('-price')  # По убыванию
    context = {
        'category': category,
        "products": products,
        'subcategories': subcategories
    }
    return render(request, 'product/catalog.html', context)
