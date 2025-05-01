from django.contrib import admin

# Register your models here.
# Register your models here.
from orders.models import Order
from orders.models import OrderItem


class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "name", "price", "quantity"
    search_fields = (
        "product",
        "name",
    )
    extra = 0

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "name", "price", "quantity"
    search_fields = (
        "order",
        "product",
        "name",
    )

class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "requires_delivery",
        "status",
        "is_paid",
        "created_timestamp",
    )

    search_fields = (
        "requires_delivery",
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        'user_username',
        'user_email',
        "requires_delivery",
        "status",
        "is_paid",
        "created_timestamp",
    )
    search_fields = (
        "id",
    )
    list_filter = (
        "requires_delivery",
        "status",
        "is_paid",
    )
    readonly_fields = ('user_username', 'user_email', 'user_first_name', 'user_last_name','user_otchestvo','user_phone', 'created_timestamp')
    fields = ('user', 'user_username', 'user_email', 'user_first_name', 'user_last_name','user_otchestvo','user_phone')
    inlines = (OrderItemTabulareAdmin,)

    def user_username(self, obj):
            return obj.user.username
    user_username.short_description = 'Логин'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'Фамилия'

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Имя'
    
    def user_otchestvo(self, obj):
        return obj.user.otchestvo
    user_otchestvo.short_description = 'Отчество'

    def user_phone(self, obj):
        return obj.user.phone
    user_phone.short_description = 'Номер телефона'