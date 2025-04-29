from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem

# Create your views here.
def create_order(request):
    form = CreateOrderForm(data=request.POST)
    if form.is_valid():
        try:
            with transaction.atomic():
                user = request.user
                cart_items = Cart.objects.filter(user=user)
                if cart_items.exists():
                    order = Order.objects.create(
                        user=user,
                        delivery_address=form.cleaned_data['delivery_address'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                    )
                    for cart_item in cart_items:
                        product=cart_item.product
                        name=cart_item.product.name
                        price=cart_item.product.price
                        quantity=cart_item.quantity
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                    cart_items.delete()
                    messages.success(request, 'Заказ оформлен!')
                    return redirect('main:index')
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('orders:create_order')
