from django.shortcuts import render
from product.models import Products
from carts.models import Cart
from django.shortcuts import redirect
# Create your views here.


def carts(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
    else:
        carts=""
    context = {
    'title': "Корзина",
    'carts': carts
    }
    return render(request, 'carts/carts.html', context)


def cart_add(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)   


def cart_change(request, product_slug):
    ...

def cart_remove(request, product_slug):
    ...