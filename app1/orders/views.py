from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from django.shortcuts import render

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
        
def orders(request):
    if request.user.is_authenticated:
        # Получаем параметр сортировки из GET-запроса (если есть)
        selected_status = request.GET.get('status', None)

        # Если выбран статус, фильтруем заказы по этому статусу, иначе все заказы
        if selected_status:
            orders = Order.objects.filter(user=request.user, status=selected_status).order_by('-created_timestamp')
        else:
            orders = Order.objects.filter(user=request.user).order_by('-created_timestamp')  # сортировка по дате создания

        # Получаем все уникальные статусы заказов
        statuses = Order.objects.values_list('status', flat=True).distinct()

        order_data = []

        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            products = [{
                'name': item.name,
                'quantity': item.quantity,
                'price': item.price,
            } for item in order_items]
            total_price = sum(item.price * item.quantity for item in order_items)

            order_data.append({
                'order_id': order.id,
                'products': products,
                'total_price': total_price,
                'delivery_method': 'Доставка' if order.requires_delivery else 'Самовывоз',
                'status': order.status,
                'is_paid': order.is_paid,
                'created_timestamp': order.created_timestamp,
            })

        context = {
            'title': "Личный кабинет",
            'orders': order_data,
            'statuses': statuses,  # Добавляем статусы в контекст
            'selected_status': selected_status,  # Сохраняем выбранный статус для отображения
        }

    return render(request, 'orders/orders.html', context)


