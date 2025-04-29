from django.contrib import admin
from orders.admin import OrderTabulareAdmin

from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines=[OrderTabulareAdmin]