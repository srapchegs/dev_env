from carts.models import Cart

def get_user_carts(request):
    return Cart.objects.filter(user=request.user)
