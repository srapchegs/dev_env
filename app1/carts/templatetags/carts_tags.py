from django import template
from carts.models import Cart
from carts.utils import get_user_carts

register = template.Library()

@register.simple_tag
def tag_cart(request):
    carts = get_user_carts(request)
    return carts.count() 