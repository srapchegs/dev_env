from django.shortcuts import render
from product.models import Products, Categories, Subcategories


# Create your views here.

def detail(request, product_slug, category_slug):
    product = Products.objects.get(slug=product_slug, category__category__slug=category_slug)
    
    if request.user.is_authenticated:
        is_in_cart = request.user.cart_set.filter(product=product).exists()
    else:
        is_in_cart = False
    
    context = {
        'title': "Детальная страница товара",
        "product": product,
        'is_in_cart': is_in_cart
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
    
    # Проверяем, аутентифицирован ли пользователь
    if request.user.is_authenticated:
        cart_products = request.user.cart_set.values_list('product', flat=True)  # Получаем все ID продуктов в корзине
        # Создаем список, в котором продукты с их флагом наличия в корзине
        product_data = [
            {
                'product': product,
                'in_cart': product.id in cart_products
            }
            for product in products
        ]
    else:
        # Если пользователь не аутентифицирован, считаем, что у него пустая корзина
        product_data = [
            {
                'product': product,
                'in_cart': False  # Нет в корзине
            }
            for product in products
        ]
    
    context = {
        'category': category,
        "products": product_data,
        'subcategories': subcategories
    }
    return render(request, 'product/catalog.html', context)
