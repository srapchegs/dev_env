import re
from django import forms


class CreateOrderForm(forms.Form):
    delivery_address = forms.CharField()
    requires_delivery = forms.ChoiceField(
    choices=[
        ("0", "Самовывоз"),
        ("1", "Доставка"),
    ],
)

