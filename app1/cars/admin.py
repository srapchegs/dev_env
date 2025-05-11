from django.contrib import admin

# Register your models here.
from cars.models import Cars, CarsBid


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CarsBid)
class CarsBidAdmin(admin.ModelAdmin):
    readonly_fields = ('user_email', 'user_first_name', 'user_last_name','user_otchestvo','user_phone', 'created_timestamp')
    fields = ('user', 'user_email', 'user_first_name', 'user_last_name','user_otchestvo','user_phone', 'cars', 'bid_address', 'date_rent')

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