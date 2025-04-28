
from django import template
from carts.models import Cart

register = template.Library()

@register.simple_tag(takes_context=True)
def tag_cart(context):
    request = context['request']
    return Cart.objects.filter(user=request.user).count()