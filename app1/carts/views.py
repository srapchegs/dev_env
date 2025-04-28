from django.shortcuts import render
from product.models import Products
from carts.models import Cart
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse
from carts.utils import get_user_carts
from django.template.loader import render_to_string
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


def cart_add(request):
    product_id = request.POST.get("product_id")
    product = Products.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    return HttpResponse(request)

def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")
    cart = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()
    user_cart = get_user_carts(request)
    context = {"carts": user_cart}
    cart_items_html = render_to_string(
        "carts/includes/include_cart.html", context, request=request)
    response_data = {
        "cart_items_html": cart_items_html,
    }
    return JsonResponse(response_data)
 
def cart_remove(request):
    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    user_cart = get_user_carts(request)
    context = {"carts": user_cart}
    cart_items_html = render_to_string(
        "carts/includes/include_cart.html", context, request=request)

    response_data = {
        "cart_items_html": cart_items_html,
    }
    return JsonResponse(response_data)